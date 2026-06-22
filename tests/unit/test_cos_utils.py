from app.utils.cos_utils import COSUtils


class FakeCOSClient:
    def __init__(self):
        self.deleted_keys = []

    def delete_object(self, Bucket, Key):  # noqa: N803 - third-party SDK naming
        self.deleted_keys.append((Bucket, Key))
        return {}


def test_generate_cos_path_applies_environment_prefix():
    cos_utils = COSUtils()
    original_prefix = cos_utils._key_prefix

    try:
        cos_utils._key_prefix = "staging/"

        path = cos_utils.generate_cos_path("dataset.csv", "datasets/csv")

        assert path.startswith("staging/datasets/csv/")
        assert path.endswith("_dataset.csv")
    finally:
        cos_utils._key_prefix = original_prefix


def test_delete_file_skips_keys_outside_allowed_prefixes():
    cos_utils = COSUtils()
    original_client = cos_utils._client
    original_bucket = cos_utils._bucket
    original_allowed_prefixes = cos_utils._delete_allowed_prefixes
    fake_client = FakeCOSClient()

    try:
        cos_utils._client = fake_client
        cos_utils._bucket = "test-bucket"
        cos_utils._delete_allowed_prefixes = ["staging/"]

        assert cos_utils.delete_file("datasets/csv/legacy.csv") is True
        assert fake_client.deleted_keys == []

        assert cos_utils.delete_file("staging/datasets/csv/new.csv") is True
        assert fake_client.deleted_keys == [
            ("test-bucket", "staging/datasets/csv/new.csv")
        ]
    finally:
        cos_utils._client = original_client
        cos_utils._bucket = original_bucket
        cos_utils._delete_allowed_prefixes = original_allowed_prefixes

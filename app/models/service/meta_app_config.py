"""
元应用配置模型
承载元应用专属字段（展示层 + 运行契约），与服务 1:1 关联。
非元应用类型不使用本表。
"""

from copy import deepcopy

from app.extensions import db


class MetaAppConfig(db.Model):
    """元应用配置模型（与 services 1:1）"""

    __tablename__ = "meta_app_configs"

    service_id = db.Column(
        db.String(36),
        db.ForeignKey("services.id", ondelete="CASCADE"),
        primary_key=True,
        comment="关联的服务ID",
    )
    # 展示层
    subtitle = db.Column(db.String(200), nullable=True, comment="元应用副标题")
    services = db.Column(db.Text, nullable=True, comment="元应用使用的服务ID列表(逗号分隔)")
    input_name = db.Column(db.String(100), nullable=True, comment="输入名称")
    output_name = db.Column(db.String(100), nullable=True, comment="输出名称")
    output_visualization = db.Column(db.Boolean, default=False, comment="是否可视化输出")
    submit_button_text = db.Column(db.String(50), nullable=True, comment="提交按钮文本")
    # 运行契约
    simulation_build_id = db.Column(db.String(64), nullable=True, comment="仿真构建ID")
    meta_app_artifact_id = db.Column(db.String(64), nullable=True, comment="元应用Artifact ID")
    meta_app_artifact_hash = db.Column(db.String(128), nullable=True, comment="元应用Artifact哈希")
    meta_app_artifact = db.Column(db.JSON, nullable=False, comment="元应用Artifact正文")
    run_mode = db.Column(db.String(32), nullable=True, comment="元应用运行模式")
    runtime_spec = db.Column(db.JSON, nullable=True, comment="元应用运行环境规格")
    # 时间戳
    create_time = db.Column(db.BigInteger, nullable=False, comment="创建时间戳")
    update_time = db.Column(db.BigInteger, nullable=True, comment="更新时间戳")

    @staticmethod
    def _services_to_list(services_str):
        if not services_str or not isinstance(services_str, str):
            return []
        return [sid.strip() for sid in services_str.split(",") if sid.strip()]

    @staticmethod
    def _services_to_string(services):
        if not isinstance(services, list):
            return None
        value = ",".join(item.strip() for item in services if isinstance(item, str) and item.strip())
        return value or None

    @staticmethod
    def _materialize_runtime_spec(runtime_spec, service_id):
        if not isinstance(runtime_spec, dict):
            return runtime_spec
        value = deepcopy(runtime_spec)
        docker = value.get("docker")
        if isinstance(docker, dict) and isinstance(docker.get("containerName"), str):
            docker["containerName"] = docker["containerName"].replace("{serviceId}", service_id)
        return value

    @classmethod
    def from_api_fields(cls, service_id, api_data, create_time):
        config = cls(
            service_id=service_id,
            simulation_build_id=api_data.get("simulationBuildId"),
            meta_app_artifact_id=api_data.get("metaAppArtifactId"),
            meta_app_artifact_hash=api_data.get("metaAppArtifactHash"),
            meta_app_artifact=api_data.get("metaAppArtifact"),
            run_mode=api_data.get("runMode"),
            runtime_spec=cls._materialize_runtime_spec(api_data.get("runtimeSpec"), service_id),
            create_time=create_time,
        )
        config.update_display_fields(api_data)
        return config

    def update_display_fields(self, api_data, update_time=None):
        self.subtitle = api_data.get("subtitle")
        self.services = self._services_to_string(api_data.get("services"))
        self.input_name = api_data.get("inputName")
        self.output_name = api_data.get("outputName")
        self.output_visualization = api_data.get("outputVisualization", False)
        self.submit_button_text = api_data.get("submitButtonText")
        if update_time is not None:
            self.update_time = update_time

    def to_api_fields(self, include_artifact=True):
        """输出合并进 apiList[0] 的元应用字段（camelCase）。"""
        fields = {
            "subtitle": self.subtitle,
            "services": self._services_to_list(self.services),
            "inputName": self.input_name,
            "outputName": self.output_name,
            "outputVisualization": bool(self.output_visualization),
            "submitButtonText": self.submit_button_text,
            "simulationBuildId": self.simulation_build_id,
            "metaAppArtifactId": self.meta_app_artifact_id,
            "metaAppArtifactHash": self.meta_app_artifact_hash,
            "runMode": self.run_mode,
            "runtimeSpec": self.runtime_spec,
        }
        if include_artifact:
            fields["metaAppArtifact"] = self.meta_app_artifact
        return fields

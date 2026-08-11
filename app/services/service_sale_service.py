"""
成果销售管理服务
提供成果销售信息的发布、更新和管理功能
"""

from app.extensions import db
from app.models.service.service import Service


class ServiceSaleError(Exception):
    """成果销售服务错误"""
    pass


class ServiceSaleService:
    """成果销售服务类"""

    @staticmethod
    def publish_service_sale(service_id, price, description):
        """
        发布销售信息

        Args:
            service_id: 成果ID
            price: 销售价格
            description: 销售说明

        Returns:
            Service: 更新后的成果对象
        """
        try:
            service = Service.query.get(service_id)
            if not service:
                raise ServiceSaleError("成果不存在")

            # 更新销售信息
            service.is_for_sale = True
            service.sale_price = price
            service.sale_description = description
            service.sale_status = 'published'

            db.session.commit()
            return service

        except Exception as e:
            db.session.rollback()
            raise ServiceSaleError(f"发布销售信息失败: {str(e)}")

    @staticmethod
    def update_service_sale_info(service_id, price=None, description=None):
        """
        更新销售信息

        Args:
            service_id: 成果ID
            price: 销售价格（可选）
            description: 销售说明（可选）

        Returns:
            Service: 更新后的成果对象
        """
        try:
            service = Service.query.get(service_id)
            if not service:
                raise ServiceSaleError("成果不存在")

            # 更新销售信息
            if price is not None:
                service.sale_price = price
            if description is not None:
                service.sale_description = description

            db.session.commit()
            return service

        except Exception as e:
            db.session.rollback()
            raise ServiceSaleError(f"更新销售信息失败: {str(e)}")

    @staticmethod
    def unpublish_service_sale(service_id):
        """
        下架销售

        Args:
            service_id: 成果ID

        Returns:
            Service: 更新后的成果对象
        """
        try:
            service = Service.query.get(service_id)
            if not service:
                raise ServiceSaleError("成果不存在")

            # 下架销售
            service.is_for_sale = False
            service.sale_status = 'unpublished'

            db.session.commit()
            return service

        except Exception as e:
            db.session.rollback()
            raise ServiceSaleError(f"下架销售失败: {str(e)}")

    @staticmethod
    def get_service_sale_info(service_id):
        """
        获取销售信息

        Args:
            service_id: 成果ID

        Returns:
            dict: 销售信息
        """
        try:
            service = Service.query.get(service_id)
            if not service:
                raise ServiceSaleError("成果不存在")

            return {
                "serviceId": service.id,
                "serviceName": service.name,
                "isForSale": service.is_for_sale,
                "salePrice": service.sale_price,
                "saleDescription": service.sale_description,
                "saleStatus": service.sale_status,
            }

        except Exception as e:
            raise ServiceSaleError(f"获取销售信息失败: {str(e)}")


# 创建全局实例
service_sale_service = ServiceSaleService()
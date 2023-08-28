from functools import wraps

from flask import request
from flask_marshmallow import Marshmallow

ma = Marshmallow()


def paginate(model, schema_class=None, sortable_fields=None):
    class DefaultSchema(ma.Schema):
        class Meta:
            fields = ('id',)

    schema_class = schema_class or DefaultSchema

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            page = int(request.args.get('page', 1))
            per_page = int(request.args.get('per_page', 10))
            sort_field = request.args.get('sort_field', 'id')
            sort_order = request.args.get('sort_order', 'asc')
            filter_field = request.args.get('filter_field')
            filter_value = request.args.get('filter_value')

            if sort_order not in ['asc', 'desc']:
                return {"error": "Invalid sort order"}, 400

            query = model.query

            if filter_field and filter_value:
                query = query.filter(getattr(model, filter_field) == filter_value)

            if sortable_fields and sort_field in sortable_fields:
                query = query.order_by(
                    getattr(model, sort_field).asc() if sort_order == 'asc' else getattr(model, sort_field).desc()
                )

            paginated_query = query.paginate(page=page, per_page=per_page)

            schema = schema_class(many=True)
            serialized_data = schema.dump(paginated_query.items)

            result = {
                "items": serialized_data,
                "page": page,
                "per_page": per_page,
                "total_pages": paginated_query.pages,
                "total_items": paginated_query.total,
            }

            return func(pagination_result=result, *args, **kwargs)

        return wrapper

    return decorator

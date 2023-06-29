from django.db.models import Count
import random
from core.models.basicProductsAndOrdersModels import Product, ProductReview, ProductRating, Order, OrderHistory, OrderItem
from core.models.utilityModels import AppSettings
from django.shortcuts import get_object_or_404
from core.models.userModels import User, UserProfile


# Statistics
class UserStatisticsService:
    @staticmethod
    def get_by_id(model, statistic_id):
        return get_object_or_404(model, id=statistic_id)

    @staticmethod
    def get_all(model):
        return model.objects.all()

    @staticmethod
    def create(model, data):
        statistic = model(**data)
        statistic.save()
        return statistic

    @staticmethod
    def update(model, statistic_id, data):
        statistic = get_object_or_404(model, id=statistic_id)
        for key, value in data.items():
            setattr(statistic, key, value)
        statistic.save()
        return statistic

    @staticmethod
    def delete(model, statistic_id):
        statistic = get_object_or_404(model, id=statistic_id)
        statistic.delete()

    @staticmethod
    def determine_model_type(request):
        # Determine the model type based on user input or any other criteria
        # You can replace this with your own logic
        user_models = [User, UserProfile, AppSettings]  # Example user models
        product_models = [Product, ProductReview, ProductRating]  # Example product models
        order_models = [Order, OrderItem, OrderHistory]  # Example order models

        if request.user.is_authenticated:
            return random.choice(user_models)
        else:
            model_type = request.GET.get('model_type')  # Example: 'product'
            if model_type is None:
                # Set a default model type here when model_type is None
                model_type = 'User'
            if model_type == 'product':
                return random.choice(product_models)
            elif model_type == 'order':
                return random.choice(order_models)
            elif model_type == 'User':
                return random.choice(user_models)
            else:
                raise ValueError("Invalid model type: {}".format(model_type))


    @staticmethod
    def create_model_instance(model_type):
        if issubclass(model_type, User):
            return UserStatisticsService.create_order_statistics()
        elif issubclass(model_type, Product):
            return UserStatisticsService.create_order_statistics()
        elif issubclass(model_type, Order):
            return UserStatisticsService.create_order_statistics()
        else:
            raise ValueError("Invalid model type")

    @staticmethod
    def create_order_statistics():
        order_statistics = {}

        # Total orders
        order_statistics['total_orders'] = Order.objects.count()

        # Total items sold
        order_statistics['total_items_sold'] = OrderItem.objects.aggregate(total_items_sold=Count('id'))['total_items_sold']

        # Average order value
        average_order_value = Order.objects.aggregate(average_order_value=models.Avg('total_amount'))
        order_statistics['average_order_value'] = round(average_order_value['average_order_value'], 2)

        # Add any other order statistics you want to calculate

        return order_statistics


# IMPLIMENTATION

# from core.models import UserStatistics
#
# service = UserStatisticsService()
# statistics = service.get_all(UserStatistics)  # Get all user statistics
# new_statistic = service.create(UserStatistics, data)  # Create a new user statistic
# updated_statistic = service.update(UserStatistics, statistic_id, data)  # Update an existing user statistic
# service.delete(UserStatistics, statistic_id)  # Delete a user statistic
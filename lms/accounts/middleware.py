from django.contrib.auth import get_user_model


User = get_user_model()

class TransitionManager:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # هذه الخطوة تتم قبل وصول الطلب إلى الفيو
        print("قبل معالجة الطلب")

        # تمرير الطلب إلى الفيو والحصول على الاستجابة
        response = self.get_response(request)

        # التحقق من وجود المستخدم
        try:
            user = User.objects.get(email=request.user.email)
            match user.role:
                case "student":
                    print("طالب")
                case "instructor":
                    print("instructor")
                case "admin":
                    print("مشرف")
                case _:
                    print("القيمة غير معروفة")
        except User.DoesNotExist:
            print("المستخدم غير موجود")
        
        print("بعد معالجة الطلب")

        return response


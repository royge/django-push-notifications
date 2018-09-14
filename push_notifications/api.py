from tastypie.authorization import Authorization
from tastypie.authentication import BasicAuthentication
from tastypie.resources import ModelResource
from .models import APNSDevice, GCMDevice, PushyDevice


class APNSDeviceResource(ModelResource):
	class Meta:
		authorization = Authorization()
		queryset = APNSDevice.objects.all()
		resource_name = "device/apns"
		filtering = {
			'name': ['exact'],
			'registration_id': ['exact']
		}


class GCMDeviceResource(ModelResource):
	class Meta:
		authorization = Authorization()
		queryset = GCMDevice.objects.all()
		resource_name = "device/gcm"
		filtering = {
			'name': ['exact'],
			'registration_id': ['exact']
		}


class APNSDeviceAuthenticatedResource(APNSDeviceResource):
	# user = ForeignKey(UserResource, "user")

	class Meta(APNSDeviceResource.Meta):
		authentication = BasicAuthentication()
		# authorization = SameUserAuthorization()

	def obj_create(self, bundle, **kwargs):
		# See https://github.com/toastdriven/django-tastypie/issues/854
		return super(APNSDeviceAuthenticatedResource, self).obj_create(bundle, user=bundle.request.user, **kwargs)


class GCMDeviceAuthenticatedResource(GCMDeviceResource):
	# user = ForeignKey(UserResource, "user")

	class Meta(GCMDeviceResource.Meta):
		authentication = BasicAuthentication()
		# authorization = SameUserAuthorization()

	def obj_create(self, bundle, **kwargs):
		# See https://github.com/toastdriven/django-tastypie/issues/854
		return super(GCMDeviceAuthenticatedResource, self).obj_create(bundle, user=bundle.request.user, **kwargs)


class PushyDeviceResource(ModelResource):
    class Meta:
        authorization = Authorization()
        queryset = PushyDevice.objects.all()
        resource_name = "device/pushy"
        filtering = {
            'name': ['exact'],
            'registration_id': ['exact'],
        }


class PushyDeviceAuthenticatedResource(PushyDeviceResource):
    class Meta(PushyDeviceResource.Meta):
        authentication = BasicAuthentication()

    def obj_create(self, bundle, **kwargs):
        # See https://github.com/toastdriven/django-tastypie/issues/854
        return super(PushyDeviceAuthenticatedResource, self).obj_create(
            bundle,
            user=bundle.request.user,
            **kwargs)
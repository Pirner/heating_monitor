from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from matplotlib import pylab
from pylab import *
import PIL, PIL.Image
from django.views.generic.list import ListView
from io import StringIO, BytesIO
from temp_monitor import models, utils
from django.utils import timezone
# Create your views here.


def index_legacy(request):
    x = 5
    template = loader.get_template('index.html')
    context = {
        'x': x,
    }
    return HttpResponse(template.render(context, request))

class IndexTempSensorListView(ListView):
    model = models.TempSensor
    template_name = 'index.html'
    temp_sensor = models.TempSensor.objects.all()
    paginate_by = 3
    # paginator = Paginator(image_list, 15)
    # scan over the "to showing images and compute their show image TODO
    utils.write_temps_to_logs()
    def get_queryset(self):
        return models.TempSensor.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

def view_sensors(request):
    utils.check_all_w1_devices()
    x = 5
    template = loader.get_template('view_sensors.html')
    context = {
        'x': x,
    }
    return HttpResponse(template.render(context, request))



def temp_plot(request):
    # Construct the graph
    utils.write_temps_to_logs()
    x = arange(0, 2*pi, 0.01)
    s = cos(x)**2
    plot(x, s)

    xlabel('xlabel(X)')
    ylabel('ylabel(Y)')
    title('Simple Graph!')
    grid(True)
    # Store image in a string buffer
    # buffer = StringIO()
    # from pudb import set_trace
    # set_trace()
    buffer = BytesIO()
    canvas = pylab.get_current_fig_manager().canvas
    canvas.draw()
    # pilImage = PIL.Image.fromstring("RGB", canvas.get_width_height(), canvas.tostring_rgb())
    pilImage = PIL.Image.frombytes("RGB", canvas.get_width_height(), canvas.tostring_rgb())
    pilImage.save(buffer, "PNG")
    pylab.close()

    # Send buffer in a http response the the browser with the mime type image/png set
    return HttpResponse(buffer.getvalue(), content_type="image/png")

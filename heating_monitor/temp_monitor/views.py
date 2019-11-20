from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from matplotlib import pylab
from pylab import *
import PIL, PIL.Image
from io import StringIO, BytesIO

# Create your views here.


def index(request):
    x = 5
    template = loader.get_template('index.html')
    context = {
        'x': x,
    }
    return HttpResponse(template.render(context, request))


def temp_plot(request):
    # Construct the graph
    # from pudb import set_trace
    # set_trace()
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

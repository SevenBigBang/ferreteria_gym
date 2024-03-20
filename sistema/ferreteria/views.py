from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from .models import Producto, CategoriaProducto
from reportlab.pdfgen import canvas
import xlwt
from django.http import HttpResponse
from .forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import render
# Vista para marcar un producto como no disponible




def producto_delete(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.disponible = False
        producto.save()
        return redirect('producto_list')
    return render(request, 'producto_confirm_delete.html', {'producto': producto})

def producto_confirm_delete(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    return render(request, 'producto_confirm_delete.html', {'producto': producto})

# Vista para generar un informe en PDF
def generate_pdf_report(request):
    try:
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="report.pdf"'

        # Genera el contenido del PDF con ReportLab
        p = canvas.Canvas(response)
        p.drawString(100, 100, "¡Este es un informe generado con ReportLab!")
        p.showPage()
        p.save()

        return response
    except Exception as e:
        return HttpResponse("Ocurrió un error al generar el informe en PDF")

# Vista para generar un informe en Excel
def generate_excel_report(request):
    try:
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="report.xls"'

        # Genera el contenido del Excel con xlwt
        workbook = xlwt.Workbook()
        sheet = workbook.add_sheet('Report')
        sheet.write(0, 0, "Este es un informe generado con Django-Excel!")

        workbook.save(response)
        return response
    except Exception as e:
        return HttpResponse("Ocurrió un error al generar el informe en Excel")

# Vista para la página de inicio
def inicio(request):
    return render(request, 'sitio/index.html')

# Vista para mostrar los productos disponibles
# Vista para mostrar los productos disponibles
def productos(request):
    try:
        productosListados = Producto.objects.filter(estado_producto='Disponible')
        categorias = CategoriaProducto.objects.all()  # Obtener todas las categorías
        data = {
            'titulo': 'Productos Disponibles',
            'productos': productosListados,
            'categorias': categorias  # Pasar las categorías al contexto
        }
        return render(request, "sitio/productos.html", data)
    except Exception as e:
        return HttpResponse("Ocurrió un error al recuperar los productos")

    

# Vista basada en clase para mostrar los productos disponibles
class ProductoListView(ListView):
    model = Producto
    template_name = 'sitio/productos.html'
    context_object_name = 'productos'

    def get_queryset(self):
        return Producto.objects.filter(estado_producto='Disponible')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Productos Disponibles'
        return context



#new
def registro(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            # Crear un nuevo usuario pero no guardarlo aún
            new_user = form.save(commit=False)
            # Llenar los campos opcionales del modelo User
            new_user.email = form.cleaned_data['email']
            new_user.first_name = form.cleaned_data['first_name']
            new_user.last_name = form.cleaned_data['last_name']
            new_user.save()
            
            return redirect('productos')  
    else:
        form = UserRegisterForm()
    context = {'form': form}
    return render(request, 'sitio/registro.html', context)

def logout_view(request):
    logout(request)
    messages.success(request, '¡Has cerrado sesión exitosamente!')
    return redirect('inicio')


def categoria(request):
    categorias = CategoriaProducto.objects.all()
    productos = Producto.objects.all()

    categoria_id = request.GET.get('categoria')
    if categoria_id:
        productos = productos.filter(id_categoria=categoria_id)

    return render(request, 'categorias.html', {'productos': productos, 'categorias': categorias})

from django.shortcuts import render
import matplotlib.pyplot as plt
import numpy as np
import io
import urllib, base64

def verificar_triangulo(request):
    contexto = {}
    if request.method == "POST":

        tipo = request.POST.get('tipo_calculo')
 
        if tipo == "lados":
            try:
                l1 = float(request.POST.get('lado1'))
                l2 = float(request.POST.get('lado2'))
                l3 = float(request.POST.get('lado3'))
                n = [l1, l2, l3]

                maior = 0
                iMaior = -1
                for i in range(len(n)):
                    if n[i] > maior:
                        maior = n[i]
                        iMaior = i

                if iMaior == 0:
                    n1, n2 = n[1], n[2]
                elif iMaior == 1:
                    n1, n2 = n[0], n[2]
                else:
                    n1, n2 = n[0], n[1]

                if (n1 + n2) > maior:
                    if (n1 == n2) and (n2 == maior):
                        resultado = "Equilátero"
                    elif (n1 == n2) or (n1 == maior) or (n2 == maior):
                        resultado = "Isósceles"
                    else:
                        resultado = "Escaleno"
                    
                    x_m = (n1**2 + maior**2 - n2**2) / (2 * maior)
                    y_m = np.sqrt(max(0, n1**2 - x_m**2))
                    
                    plt.figure(figsize=(5, 4))
                    plt.plot([0, maior, x_m, 0], [0, 0, y_m, 0], marker='o')
                    plt.fill([0, maior, x_m, 0], [0, 0, y_m, 0], alpha=0.3)
                    plt.axis('equal')
                    plt.grid(True, linestyle='--', alpha=0.6)
                    
                    buf = io.BytesIO()
                    plt.savefig(buf, format='png')
                    buf.seek(0)
                    string = base64.b64encode(buf.read())
                    uri = urllib.parse.quote(string)
                    
                    contexto = {'resultado': resultado, 'grafico': uri}
                    plt.close() 
                else:
                    contexto = {'erro': "As medidas não formam um triângulo"}
            except (ValueError, TypeError):
                    contexto = {'erro': "Por favor, insira números válidos nos lados."}

        elif tipo == "angulos":
            try:
                a1 = float(request.POST.get('angulo1'))
                a2 = float(request.POST.get('angulo2'))
                a3 = float(request.POST.get('angulo3'))
                n = [a1, a2, a3]

                if (a1 + a2 + a3) == 180 and all(a > 0 for a in [a1, a2, a3]):
                    if (a1 == a2) and (a2 == a3):
                        resultado = "Equilátero"
                    elif (a1 == a2) or (a1 == a3) or (a2 == a3):
                        resultado = "Isósceles"
                    else:
                        resultado = "Escaleno"

                    rad_a1 = np.radians(a1)
                    rad_a2 = np.radians(a2)
                    
                    c = 10 
                    rad_a3 = np.radians(a3)
                    a = c * np.sin(rad_a2) / np.sin(rad_a3)

                    x_c = a * np.cos(rad_a1)
                    y_c = a * np.sin(rad_a1)

                    pontos_x = [0, c, x_c, 0]
                    pontos_y = [0, 0, y_c, 0]

                    plt.figure(figsize=(5, 4))
                    plt.plot(pontos_x, pontos_y, marker='o')
                    plt.fill(pontos_x, pontos_y, alpha=0.3)
                    
                    plt.text(0.5, 0.5, f'{a1}°', fontsize=12, color='darkblue')
                    plt.text(c - 1.5, 0.5, f'{a2}°', fontsize=12, color='darkblue')
                    plt.text(x_c, y_c - 1.5, f'{a3}°', fontsize=12, color='darkblue', ha='center')

                    plt.axis('equal')
                    plt.grid(True, linestyle='--', alpha=0.6)
                    plt.title(f"Ângulos: {a1}°, {a2}°, {a3}°")
                    
                    buf = io.BytesIO()
                    plt.savefig(buf, format='png')
                    buf.seek(0)
                    string = base64.b64encode(buf.read())
                    uri = urllib.parse.quote(string)
                    
                    contexto = {'resultado': resultado, 'grafico': uri}
                    plt.close()
                else:
                    contexto = {'erro': "As medidas não formam um triângulo"}
            except (ValueError, TypeError):
                contexto = {'erro': "Por favor, insira números válidos nos ângulos."}
                
    return render(request, 'triangulo.html', contexto)
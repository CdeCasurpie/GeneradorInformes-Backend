<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>INFORME DE INSPECCIÓN TÉCNICA</title>
  <style>
    .logo {
      text-align: right;
      margin-bottom: 20px;
    }
    .logo img {
      width: 100px;
    }
    .title {
      text-align: center;
      color: #7a98b5;
      font-size: 28px;
      margin: 40px 0;
    }
    .section-header {
      background-color: #7a98b5;
      color: white;
      padding: 10px;
      margin: 20px 0 15px 0;
      font-weight: bold;
    }
    .data-table {
      width: 100%;
      border-collapse: collapse;
    }
    .data-table td {
      padding: 10px;
      border-bottom: 1px solid #ddd;
    }
    .highlight {
      background-color: yellow;
      padding: 2px 5px;
      font-weight: bold;
    }
    .images-row {
      display: flex;
      justify-content: space-between;
      margin: 15px 0;
      flex-wrap: wrap;
    }
    .images-row img {
      max-width: 23%;
      margin-bottom: 10px;
    }
    .technician {
      margin-bottom: 30px;
    }
    .bullet {
      margin-left: 20px;
      position: relative;
    }
    .bullet::before {
      content: "■";
      position: absolute;
      left: -20px;
    }
    .arrow {
      margin-left: 20px;
      position: relative;
    }
    .arrow::before {
      content: "➢";
      position: absolute;
      left: -20px;
    }
    .page-number {
      text-align: left;
      margin-top: 50px;
      color: #666;
      font-size: 12px;
    }
    .footer {
      margin-top: 50px;
      text-align: center;
    }
    .signature-line {
      text-align: center;
      border-top: 1px solid #000;
      width: 200px;
      margin: 10px auto;
      padding-top: 5px;
    }
  </style>
</head>
<body>
  <div class="logo">
    <img src="http://localhost:5000/static/" alt="Logo Claro" />
  </div>

  <h1 class="title">INFORME DE INSPECCIÓN TÉCNICA</h1>

  <div class="section-header">DATOS GENERALES</div>

  <table class="data-table">
    <tr>
      <td width="33%" ><strong>FECHA DEL INSPECCION</strong></td>
      <td width="33%"><strong>NOMBRE CONTRATA</strong></td>
      <td width="33%"><strong>PREPARADO POR:</strong></td>
    </tr>
    <tr>
      <td>26 de noviembre de 2024</td>
      <td>DIMERA SERVICIO MULTIPLES SAC</td>
      <td>Malcolm Valdivia Berroa</td>
    </tr>
  </table>

  <div class="section-header">RESUMEN</div>

  <p class="arrow">Se realiza inspección Técnica a los técnicos de Instalaciones y Mantenimiento FTTH y HFC de la contratista DIMERA - Arequipa encontrando las siguientes observaciones;</p>

  <div class="technician">
    <p class="bullet">Técnico Franki Pacheco Mamani</p>
    <p><span class="highlight">Uniforme en mal estado (Polo)</span></p>
    <div class="images-row">
      <img src="/api/placeholder/200/300" alt="Técnico Franki Pacheco" />
      <img src="/api/placeholder/200/300" alt="Detalle polo dañado 1" />
      <img src="/api/placeholder/200/300" alt="Detalle polo dañado 2" />
      <img src="/api/placeholder/200/300" alt="Detalle polo dañado 3" />
    </div>
  </div>

  <div class="technician">
    <p class="bullet">Técnico Cesar Alanguia Mamani</p>
    <p><span class="highlight">Uniforme en mal estado (Pantalón-Polo)</span></p>
    <div class="images-row">
      <img src="/api/placeholder/200/300" alt="Técnico Cesar Alanguia" />
      <img src="/api/placeholder/200/300" alt="Detalle pantalón dañado" />
      <img src="/api/placeholder/200/300" alt="Detalle polo dañado" />
    </div>
  </div>

  <div class="technician">
    <p class="bullet">Técnico Dennis Montalvo Hurtado</p>
    <p><span class="highlight">Uniforme en mal estado (Pantalón-Polo)</span></p>
    <div class="images-row">
      <img src="/api/placeholder/200/300" alt="Técnico Dennis Montalvo" />
      <img src="/api/placeholder/200/300" alt="Detalle pantalón dañado" />
      <img src="/api/placeholder/200/300" alt="Detalle polo dañado" />
    </div>
  </div>

  <div class="page-number">Página 2</div>

  <div class="technician">
    <p class="bullet">Técnico Anthony Ninataype Ninataype</p>
    <p><span class="highlight">Uniforme en mal estado (Pantalón)</span> <span class="highlight">Calzado de Seguridad en mal estado</span></p>
    <div class="images-row">
      <img src="/api/placeholder/200/300" alt="Técnico Anthony Ninataype" />
      <img src="/api/placeholder/200/300" alt="Detalle calzado dañado" />
    </div>
  </div>

  <div class="technician">
    <p class="bullet">Técnico Jose Valero Delgado</p>
    <p><span class="highlight">Uniforme en mal estado (Pantalón)</span></p>
    <div class="images-row">
      <img src="/api/placeholder/200/300" alt="Técnico Jose Valero" />
      <img src="/api/placeholder/200/300" alt="Detalle pantalón dañado" />
    </div>
  </div>

  <div class="page-number">Página 3</div>

  <div class="section-header">HISTORIAL DE RIESGOS Y PROBLEMAS</div>

  <p>INSPECCIÓN REALIZADA 26/11/2024</p>

  <div class="section-header">CONCLUSIONES/RECOMENDACIONES</div>

  <ul>
    <li>Se recomienda a la contratista verificar permanentemente el uniforme que este en buen estado para la atención de los clientes</li>
    <li>Verificar Elementos de Protección Personal y Elementos de Protección Externa para evitar accidentes.</li>
  </ul>

  <div class="footer">
    <p>---------------------------------</p>
    <p>Superv. Malcolm Valdivia</p>
  </div>

  <div class="page-number">Página 4</div>
</body>
</html>
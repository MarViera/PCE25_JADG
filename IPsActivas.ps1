# Obtener todas las conexiones de red activas
$connections = Get-NetTCPConnection | Select-Object -ExpandProperty RemoteAddress

# Filtrar para eliminar valores vacíos y evitar repetir IPs
$uniqueIPs = $connections | Where-Object { $_ -match "\d+\.\d+\.\d+\.\d+" } | Sort-Object -Unique

# Imprimir la lista de IPs establecidas
Write-Host $uniqueIPs 

# Opcional: Guardar la lista en un archivo de texto
$uniqueIPs | Out-File -FilePath "ConexionesIPs.txt"

# Generador de Currículums mediante IA

## Backend (Docker)
- Para levantar el proyecto: `docker-compose up --build`
- Para parar: `docker-compose down`
- Para parar y borrar datos: `docker-compose down -v`

Disponible en: http://localhost:8001
Documentación API (Swagger): http://localhost:8001/docs

## Frontend
```bash
npm install
npm install vue
npm install html2pdf.js
npm run dev
```

> ⚠️ **Windows:** si `npm` da error de "ejecución de scripts deshabilitada", abre PowerShell como administrador y ejecuta:
> ```powershell
> Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```
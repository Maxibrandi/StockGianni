# Imagen base ligera de Node.js
FROM node:20-alpine

WORKDIR /app

# Copiar manifiestos e instalar dependencias
COPY package*.json ./
RUN npm install

# Copiar el resto del código del frontend
COPY . .

# Exponer el puerto predeterminado de Vite
EXPOSE 5173

# Correr el servidor de desarrollo escuchando en todas las interfaces de red
CMD ["npm", "run", "dev", "--", "--host"]
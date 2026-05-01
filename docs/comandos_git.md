# 1. Verifica qué ha cambiado

git status

# 2. Añade los archivos modificados

git add .

# 3. Confirma con un mensaje claro

git commit -m "tipo: descripción breve"

# 4. Sube a GitHub

git push origin main



**📌 ****Tip para mensajes de commit profesionales:**

| `feat:`     | **Nueva funcionalidad**                          | `feat: agregar filtro por precio en CSV`    |
| ------------- | ------------------------------------------------------ | --------------------------------------------- |
| `fix:`      | **Corrección de bug**                           | `fix: corregir ruta relativa en leer_csv`   |
| `docs:`     | **Cambios en documentación**                    | `docs: añadir apuntes sobre pathlib`       |
| `chore:`    | **Mantenimiento, config**                        | `chore: actualizar .gitignore`              |
| `refactor:` | **Mejora de código sin cambiar comportamiento** | `refactor: extraer función de validación` |



### 📥 Para BAJAR cambios (en la otra máquina)


# 1. Asegúrate de estar en la rama correcta

git branch  # Debe marcar * main

# 2. Trae los cambios desde GitHub

git pull origin main

# 3. (Opcional) Verifica que todo está actualizado

git status  # Debe decir "Your branch is up to date"



**⚠️ ****Si tienes cambios locales sin commitear** y Git te avisa que hay conflicto:


# Opción A: Guarda tus cambios temporalmente

git stash
git pull origin main
git stash pop  # Recupera tus cambios después del pull

# Opción B: Haz commit primero (recomendado)

git add .
git commit -m "wip: cambios en progreso"
git pull origin main



### 🧰 Script rápido de sincronización (copia y pega)

**Guárdalo en **`docs/comandos_git.md` para tenerlo siempre a mano:


## 🚀 SUBIR cambios (antes de cambiar de máquina)

git status
git add .
git commit -m "tipo: Actualizacion del proyecto"
git push origin main

## 📥 BAJAR cambios (al empezar en una nueva máquina)

git pull origin main
git status  # Verificar que está "up to date"

## 🔍 Verificar estado

git status          # Cambios locales
git log -3          # Últimos 3 commits
git remote -v       # Conexión con GitHub

## 🆘 Si hay conflicto

git stash           # Guarda cambios temporalmente
git pull origin main
git stash pop       # Recupera cambios

# Resolver conflictos manualmente en los archivos marcados

git add .
git commit -m "fix: resolver conflicto de merge"

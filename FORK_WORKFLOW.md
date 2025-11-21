# Fork Workflow - Mantener Tu Proyecto Actualizado

Esta guía te muestra cómo crear tu propio proyecto basado en este template mientras mantienes la capacidad de recibir actualizaciones y correcciones del repositorio original.

---

## 📋 Tabla de Contenidos

1. [Setup Inicial - Fork + Upstream](#setup-inicial---fork--upstream)
2. [Levantar el Proyecto en Local](#levantar-el-proyecto-en-local)
3. [Workflow Diario](#workflow-diario)
4. [Obtener Actualizaciones del Template](#obtener-actualizaciones-del-template)
5. [Resolver Conflictos](#resolver-conflictos)
6. [Escenarios Comunes](#escenarios-comunes)
7. [Troubleshooting](#troubleshooting)
8. [Contribuir al Proyecto Original (Pull Requests)](#-contribuir-al-proyecto-original-pull-requests) ⭐ NUEVO

---

## 🚀 Setup Inicial - Fork + Upstream

### Paso 1: Hacer Fork en GitHub

1. Ve a https://github.com/dinnovos/agent-base-project
2. Haz click en el botón **"Fork"** (esquina superior derecha)
3. Selecciona tu cuenta o organización
4. Espera a que GitHub cree tu fork
5. Ahora tienes tu propia copia en: `https://github.com/TU_USUARIO/agent-base-project`

### Paso 2: Clonar Tu Fork

Clona **TU fork** (no el repositorio original):

**Windows (PowerShell):**
```powershell
# Usando HTTPS
git clone https://github.com/TU_USUARIO/agent-base-project.git
cd agent-base-project
```

**Linux/macOS:**
```bash
# Usando HTTPS
git clone https://github.com/TU_USUARIO/agent-base-project.git
cd agent-base-project

# O usando SSH (si tienes configurado)
git clone git@github.com:TU_USUARIO/agent-base-project.git
cd agent-base-project
```

### Paso 3: Configurar Remote Upstream

Agrega el repositorio original como "upstream" para poder recibir actualizaciones:

```bash
# Agregar el repositorio original como upstream
git remote add upstream https://github.com/dinnovos/agent-base-project.git

# Verificar que tienes ambos remotes configurados
git remote -v
```

**Deberías ver algo como:**
```
origin    https://github.com/TU_USUARIO/agent-base-project.git (fetch)
origin    https://github.com/TU_USUARIO/agent-base-project.git (push)
upstream  https://github.com/dinnovos/agent-base-project.git (fetch)
upstream  https://github.com/dinnovos/agent-base-project.git (push)
```

**Explicación:**
- **origin**: Tu fork (donde haces push de tus cambios)
- **upstream**: El repositorio original (de donde obtienes actualizaciones)

---

## 💻 Levantar el Proyecto en Local

### Paso 1: Instalar uv (si no lo tienes)

**Windows (PowerShell):**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Linux/macOS:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Verificar instalación:**
```bash
uv --version
```

### Paso 2: Instalar Dependencias

```bash
# Esto crea el entorno virtual (.venv) e instala todas las dependencias
uv sync
```

**Qué hace esto:**
- ✅ Crea `.venv/` automáticamente
- ✅ Instala todos los paquetes de `pyproject.toml`
- ✅ Es 10-100x más rápido que pip

### Paso 3: Configurar Variables de Entorno

**Windows:**
```powershell
copy .env.example .env
```

**Linux/macOS:**
```bash
cp .env.example .env
```

**Edita el archivo `.env`** con tus configuraciones:

```env
# Base de datos (SQLite para desarrollo local)
DATABASE_URL=sqlite:///./app.db

# Genera una clave secreta segura
SECRET_KEY=tu-clave-secreta-aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Bcrypt (10 rondas para desarrollo)
BCRYPT_ROUNDS=10

# Rate Limiting
CHATBOT_QUERY_LIMIT=5
CHATBOT_QUERY_WINDOW_HOURS=24

# OpenAI (REQUERIDO para el chatbot)
OPENAI_API_KEY=sk-tu-api-key-aqui

# LangSmith (OPCIONAL - para tracing)
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=lsv2_tu-api-key-aqui
```

**Generar SECRET_KEY seguro:**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

**Obtener API Keys:**
- **OpenAI**: https://platform.openai.com/api-keys
- **LangSmith** (opcional): https://smith.langchain.com/

### Paso 4: Inicializar la Base de Datos

```bash
# Crear la migración inicial
alembic revision --autogenerate -m "initial migration"

# Aplicar la migración (crea las tablas)
alembic upgrade head
```

**Esto crea:**
- Tabla `users` - Usuarios del sistema
- Tabla `profiles` - Perfiles de usuario
- Tabla `usage_logs` - Logs de uso del chatbot
- Tablas de checkpoint para LangGraph

### Paso 5: Ejecutar la Aplicación

**Windows:**
```powershell
python run.py
```

**Linux/macOS:**
```bash
python run.py
# o
uvicorn src.main:app --reload
```

**Deberías ver:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

### Paso 6: Verificar que Funciona

Abre tu navegador y visita:

- **API Docs (Swagger)**: http://localhost:8000/docs
- **API Docs (ReDoc)**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

**Si ves la documentación de la API, ¡todo está funcionando!** 🎉

---

## 💼 Workflow Diario

### Trabajar en Tu Proyecto

```bash
# 1. Asegúrate de estar en la rama main
git checkout main

# 2. Crea una rama para tu nueva feature (recomendado)
git checkout -b feature/mi-nueva-funcionalidad

# 3. Haz tus cambios
# ... edita archivos, agrega código ...

# 4. Commitea tus cambios
git add .
git commit -m "feat: agrego funcionalidad X"

# 5. Push a TU fork
git push origin feature/mi-nueva-funcionalidad

# 6. Cuando esté listo, merge a main
git checkout main
git merge feature/mi-nueva-funcionalidad
git push origin main
```

### Ejecutar el Servidor Durante Desarrollo

```bash
# Activar entorno virtual (si no está activado)
# Windows
.venv\Scripts\activate

# Linux/macOS
source .venv/bin/activate

# Ejecutar servidor (con auto-reload)
python run.py
```

El servidor se recargará automáticamente cuando hagas cambios en el código.

---

## 🔄 Obtener Actualizaciones del Template

### Método 1: Merge Completo (Recomendado)

Trae **TODOS** los cambios del repositorio original:

```bash
# 1. Asegúrate de tener todo commiteado
git status  # Debe estar limpio

# 2. Ve a la rama main
git checkout main

# 3. Obtén los cambios del upstream
git fetch upstream

# 4. (Opcional) Ve qué cambios hay
git log HEAD..upstream/main --oneline

# 5. Merge los cambios
git merge upstream/main

# 6. Si hay conflictos, resuélvelos (ver sección abajo)

# 7. Push a tu fork
git push origin main
```

### Método 2: Cherry-Pick Selectivo

Trae **SOLO** commits específicos que te interesen:

```bash
# 1. Fetch cambios del upstream
git fetch upstream

# 2. Ve los commits disponibles
git log upstream/main --oneline -20

# 3. Identifica el commit que quieres
# Ejemplo: abc1234 fix: corrige bug de autenticación

# 4. Aplica solo ese commit
git cherry-pick abc1234

# 5. Push a tu fork
git push origin main
```

### Cuándo Actualizar

**Actualiza cuando:**
- ✅ Hay correcciones de bugs críticos
- ✅ Hay parches de seguridad
- ✅ Hay nuevas features que necesitas
- ✅ Mensualmente (mantenimiento regular)

**No actualices si:**
- ❌ Estás en medio de un desarrollo importante
- ❌ Los cambios no son relevantes para tu proyecto
- ❌ Tu proyecto ha divergido mucho del template

---

## 🔧 Resolver Conflictos

Los conflictos ocurren cuando tú y el upstream modificaron las mismas líneas de código.

### Paso 1: Identificar Conflictos

```bash
git merge upstream/main
# Auto-merging src/main.py
# CONFLICT (content): Merge conflict in src/main.py
# Automatic merge failed; fix conflicts and then commit the result.
```

### Paso 2: Ver Archivos en Conflicto

```bash
git status
# Unmerged paths:
#   both modified:   src/main.py
#   both modified:   src/routers/chatbot.py
```

### Paso 3: Abrir y Resolver Conflictos

Abre cada archivo en conflicto. Verás marcadores como estos:

```python
<<<<<<< HEAD
# Tu código
def mi_funcion():
    return "mi versión"
=======
# Código del upstream
def mi_funcion():
    return "versión del template"
>>>>>>> upstream/main
```

**Edita el archivo** para quedarte con lo que necesitas:

```python
# Opción A: Quedarte con tu versión
def mi_funcion():
    return "mi versión"

# Opción B: Quedarte con la versión upstream
def mi_funcion():
    return "versión del template"

# Opción C: Combinar ambas (lo más común)
def mi_funcion():
    # Combino lo mejor de ambas versiones
    return "versión mejorada"
```

**Elimina los marcadores** `<<<<<<<`, `=======`, `>>>>>>>`.

### Paso 4: Completar el Merge

```bash
# Marca los archivos como resueltos
git add src/main.py
git add src/routers/chatbot.py

# Completa el merge
git commit -m "merge: actualización desde upstream con conflictos resueltos"

# Push a tu fork
git push origin main
```

### Paso 5: Probar que Todo Funciona

```bash
# Ejecuta el servidor
python run.py

# Ejecuta los tests
pytest

# Verifica que todo funciona correctamente
```

---

## 📋 Escenarios Comunes

### Escenario 1: Bug Fix en el Template

**Situación:** Se corrigió un bug de seguridad en el template original.

```bash
# 1. Fetch y merge
git fetch upstream
git merge upstream/main

# 2. Prueba que funciona
python run.py
pytest

# 3. Push
git push origin main
```

### Escenario 2: Nueva Feature en el Template

**Situación:** Se agregó una nueva funcionalidad que quieres usar.

```bash
# 1. Fetch cambios
git fetch upstream

# 2. Revisa los cambios
git log upstream/main --oneline -10

# 3. Merge
git merge upstream/main

# 4. Actualiza tu .env si hay nuevas variables
diff .env.example .env

# 5. Actualiza la base de datos si hay migraciones
alembic upgrade head

# 6. Prueba
python run.py

# 7. Push
git push origin main
```

### Escenario 3: Cambio que NO Quieres

**Situación:** Hay un cambio en upstream que no necesitas o no quieres.

**Opción A:** No hagas merge, mantén tu versión
```bash
# Simplemente no hagas merge
# Continúa trabajando normalmente
```

**Opción B:** Merge pero revierte ese cambio específico
```bash
# Merge todo
git merge upstream/main

# Revierte el commit específico que no quieres
git revert abc1234

# Push
git push origin main
```

**Opción C:** Usa cherry-pick para cambios selectivos
```bash
# Solo toma los commits que necesitas
git cherry-pick def5678  # Bug fix que sí quieres
git cherry-pick ghi9012  # Security patch que sí quieres
# Ignora el commit que no quieres

git push origin main
```

### Escenario 4: Tu Proyecto Ha Divergido Mucho

**Situación:** Has hecho muchos cambios y el merge es muy complicado.

```bash
# Usa cherry-pick para cambios críticos solamente
git fetch upstream
git log upstream/main --oneline

# Solo toma security patches y bug fixes críticos
git cherry-pick abc1234  # Security fix
git cherry-pick def5678  # Critical bug fix

# Ignora features nuevas que causarían conflictos
git push origin main
```

---

## 🛠️ Comandos Útiles

### Ver Diferencias con Upstream

```bash
# Ver commits que upstream tiene y tú no
git log HEAD..upstream/main --oneline

# Ver commits que tú tienes y upstream no
git log upstream/main..HEAD --oneline

# Ver diferencias en archivos específicos
git diff upstream/main src/main.py
```

### Ver Historial

```bash
# Ver historial de merges
git log --merges --oneline

# Ver gráfico de branches
git log --graph --oneline --all --decorate

# Ver último commit de upstream
git fetch upstream
git log upstream/main -1
```

### Verificar Estado

```bash
# Estado actual
git status

# Remotes configurados
git remote -v

# Branches locales y remotos
git branch -a
```

---

## 🆘 Troubleshooting

### Error: "fatal: 'upstream' does not appear to be a git repository"

**Causa:** No has agregado el upstream.

**Solución:**
```bash
git remote add upstream https://github.com/dinnovos/agent-base-project.git
git remote -v  # Verificar
```

### Error: "Your local changes would be overwritten by merge"

**Causa:** Tienes cambios sin commitear.

**Solución:**
```bash
# Opción A: Commitear cambios
git add .
git commit -m "wip: trabajo en progreso"
git merge upstream/main

# Opción B: Guardar temporalmente (stash)
git stash
git merge upstream/main
git stash pop  # Recuperar cambios
```

### Error: "Merge conflict in multiple files"

**Causa:** Múltiples archivos tienen conflictos.

**Solución:**
```bash
# 1. Ver archivos en conflicto
git status

# 2. Resolver cada archivo uno por uno
# Edita cada archivo, quita los marcadores <<<<< ===== >>>>>

# 3. Marca cada archivo como resuelto
git add archivo1.py
git add archivo2.py

# 4. Completa el merge
git commit
```

### Error: "Cannot merge unrelated histories"

**Causa:** Los historiales de Git son completamente diferentes.

**Solución:**
```bash
git merge upstream/main --allow-unrelated-histories
```

### Error: "Psycopg cannot use the 'ProactorEventLoop'" (Windows)

**Causa:** Problema específico de Windows con psycopg.

**Solución:**
```bash
# Usa run.py en lugar de uvicorn directo
python run.py

# O usa uvicorn con el parámetro --loop
uvicorn src.main:app --reload --loop asyncio
```

### Error: "OpenAI API key not found"

**Causa:** No has configurado la API key.

**Solución:**
```bash
# Edita .env y agrega:
OPENAI_API_KEY=sk-tu-api-key-aqui
```

---

## ✅ Checklist de Mantenimiento Mensual

Usa esto para mantener tu fork actualizado:

- [ ] Fetch cambios de upstream: `git fetch upstream`
- [ ] Revisar nuevos commits: `git log HEAD..upstream/main --oneline`
- [ ] Leer el changelog o release notes del upstream
- [ ] Decidir si hacer merge o cherry-pick
- [ ] Hacer backup de tu base de datos (si es importante)
- [ ] Merge o cherry-pick: `git merge upstream/main`
- [ ] Resolver conflictos si los hay
- [ ] Actualizar .env con nuevas variables si las hay
- [ ] Ejecutar migraciones: `alembic upgrade head`
- [ ] Probar la aplicación: `python run.py`
- [ ] Ejecutar tests: `pytest`
- [ ] Push a tu fork: `git push origin main`
- [ ] Documentar cambios en tu CHANGELOG.md

---

## 🎓 Ejemplo Completo Paso a Paso

### Situación Real

Imagina que:
1. Hiciste fork hace 2 meses
2. Has agregado 5 nuevas features a tu proyecto
3. El template original corrigió un bug de seguridad importante
4. También agregaron una nueva feature que te interesa
5. Quieres obtener ambas actualizaciones

### Solución Completa

```bash
# ===== PREPARACIÓN =====

# 1. Verifica que todo está commiteado
git status
# Si hay cambios sin commitear:
git add .
git commit -m "wip: guardar trabajo actual"

# 2. Ve a la rama main
git checkout main

# 3. Asegúrate de tener la última versión de tu fork
git pull origin main

# ===== OBTENER ACTUALIZACIONES =====

# 4. Fetch cambios del upstream
git fetch upstream

# 5. Ve qué cambios hay
git log HEAD..upstream/main --oneline
# Ves:
# abc1234 fix: security patch for authentication
# def5678 feat: add new rate limiting feature
# ghi9012 docs: update README

# 6. Merge los cambios
git merge upstream/main

# ===== RESOLVER CONFLICTOS (si los hay) =====

# 7. Si hay conflictos, Git te avisará
# CONFLICT (content): Merge conflict in src/routers/chatbot.py

# 8. Abre el archivo y resuelve
code src/routers/chatbot.py  # o tu editor preferido

# 9. Busca los marcadores y resuelve
# Edita el archivo, elimina <<<<< ===== >>>>>

# 10. Marca como resuelto
git add src/routers/chatbot.py

# 11. Completa el merge
git commit -m "merge: actualización desde upstream con security patch"

# ===== ACTUALIZAR CONFIGURACIÓN =====

# 12. Compara .env con .env.example
diff .env.example .env

# 13. Agrega nuevas variables si las hay
# Edita .env manualmente

# 14. Ejecuta migraciones si las hay
alembic upgrade head

# ===== PROBAR =====

# 15. Ejecuta el servidor
python run.py

# 16. Prueba en el navegador
# http://localhost:8000/docs

# 17. Ejecuta los tests
pytest

# ===== FINALIZAR =====

# 18. Si todo funciona, push a tu fork
git push origin main

# 19. Verifica en GitHub que tu fork está actualizado
# Ve a: https://github.com/TU_USUARIO/agent-base-project
```

---

## 🎯 Resumen Visual

```
┌─────────────────────────────────────────────────────────────┐
│                    WORKFLOW COMPLETO                         │
└─────────────────────────────────────────────────────────────┘

1. SETUP INICIAL (una vez)
   ├─ Fork en GitHub
   ├─ Clonar tu fork
   ├─ Agregar upstream
   ├─ Instalar dependencias (uv sync)
   ├─ Configurar .env
   ├─ Inicializar BD (alembic upgrade head)
   └─ Ejecutar (python run.py)

2. TRABAJO DIARIO
   ├─ Crear rama feature
   ├─ Hacer cambios
   ├─ Commitear
   └─ Push a origin

3. ACTUALIZAR DESDE UPSTREAM (mensual)
   ├─ git fetch upstream
   ├─ git merge upstream/main
   ├─ Resolver conflictos
   ├─ Probar
   └─ git push origin main

4. MANTENER
   ├─ Revisar cambios upstream regularmente
   ├─ Aplicar security patches inmediatamente
   ├─ Evaluar nuevas features
   └─ Documentar tus cambios
```

---

## 🤝 Contribuir al Proyecto Original (Pull Requests)

Una de las ventajas principales de hacer fork es que puedes **contribuir mejoras al proyecto original** mediante Pull Requests (PRs).

### Cuándo Hacer un PR

Haz un PR cuando:
- ✅ Encuentres y corrijas un bug
- ✅ Agregues una feature útil para otros
- ✅ Mejores la documentación
- ✅ Optimices el código
- ✅ Corrijas problemas de seguridad

**NO hagas PR si:**
- ❌ Es una customización específica para tu proyecto
- ❌ Cambios que solo te benefician a ti
- ❌ Código que no está bien probado

### Paso 1: Crear una Rama para Tu Contribución

```bash
# Asegúrate de estar en main y actualizado
git checkout main
git pull origin main

# Crea una rama descriptiva para tu cambio
git checkout -b fix/bug-autenticacion
# o
git checkout -b feature/mejorar-rate-limiting
# o
git checkout -b docs/actualizar-readme
```

**Convención de nombres:**
- `fix/` - Para correcciones de bugs
- `feature/` - Para nuevas features
- `docs/` - Para cambios de documentación
- `perf/` - Para optimizaciones de rendimiento
- `security/` - Para parches de seguridad

### Paso 2: Hacer Tus Cambios

```bash
# 1. Edita los archivos necesarios
# ... haz tus cambios ...

# 2. Prueba localmente
python run.py
pytest

# 3. Commitea tus cambios
git add .
git commit -m "fix: corrige bug de autenticación en chatbot

- Describe el problema que corregiste
- Explica cómo lo corregiste
- Menciona si hay breaking changes"
```

**Buenas prácticas para commits:**
- ✅ Commits pequeños y enfocados
- ✅ Mensajes descriptivos
- ✅ Referencia a issues si existen
- ✅ Pruebas incluidas

### Paso 3: Push a Tu Fork

```bash
# Push tu rama a tu fork
git push origin fix/bug-autenticacion
```

### Paso 4: Crear el Pull Request en GitHub

1. Ve a tu fork en GitHub: `https://github.com/TU_USUARIO/agent-base-project`
2. Verás un banner amarillo que dice "Compare & pull request"
3. Click en ese botón
4. **O** ve a "Pull requests" → "New pull request"

### Paso 5: Llenar la Información del PR

**Título del PR:**
```
fix: corrige bug de autenticación en chatbot
```

**Descripción del PR:**
```markdown
## Descripción
Corrige el bug donde los usuarios no podían autenticarse correctamente
cuando usaban caracteres especiales en la contraseña.

## Problema
- Describe el problema que encontraste
- Por qué es importante corregirlo
- Qué impacto tiene

## Solución
- Explica cómo lo corregiste
- Qué cambios hiciste
- Por qué es la mejor solución

## Cambios
- [ ] Corrección de bug
- [ ] Nueva feature
- [ ] Cambio de documentación
- [ ] Cambio de configuración

## Testing
- [ ] Probé localmente
- [ ] Ejecuté los tests
- [ ] Agregué tests nuevos
- [ ] No hay breaking changes

## Checklist
- [x] Mi código sigue el estilo del proyecto
- [x] He actualizado la documentación
- [x] He agregado tests si es necesario
- [x] Todos los tests pasan
- [x] No hay conflictos con main

## Screenshots (si aplica)
Si es un cambio visual, agrega screenshots.

## Issues Relacionados
Cierra #123 (si hay un issue relacionado)
```

### Paso 6: Esperar Revisión

El mantenedor del proyecto:
- 👀 Revisará tu código
- 💬 Puede pedir cambios
- ✅ Aprobará y mergeará si todo está bien

**Si piden cambios:**
```bash
# 1. Haz los cambios solicitados
# ... edita archivos ...

# 2. Commitea los cambios
git add .
git commit -m "review: responder comentarios de revisión"

# 3. Push a la misma rama
git push origin fix/bug-autenticacion

# El PR se actualiza automáticamente
```

### Paso 7: ¡Tu PR fue Mergeado!

```bash
# 1. Vuelve a main
git checkout main

# 2. Actualiza desde upstream
git fetch upstream
git merge upstream/main

# 3. Borra la rama local
git branch -d fix/bug-autenticacion

# 4. Borra la rama remota
git push origin --delete fix/bug-autenticacion
```

---

## 📋 Ejemplo Completo: Contribuir un Bug Fix

### Situación
Encontraste un bug en el rate limiting del chatbot y quieres contribuir la corrección.

### Paso a Paso

```bash
# ===== PREPARACIÓN =====

# 1. Asegúrate de tener todo actualizado
git checkout main
git pull origin main
git fetch upstream
git merge upstream/main

# ===== CREAR RAMA =====

# 2. Crea rama para el fix
git checkout -b fix/rate-limit-off-by-one

# ===== HACER CAMBIOS =====

# 3. Edita el archivo con el bug
code src/services/usage_log_service.py

# 4. Haz los cambios necesarios
# ... edita el código ...

# ===== PROBAR =====

# 5. Prueba localmente
python run.py

# 6. Ejecuta los tests
pytest

# 7. Crea un test para el bug (si no existe)
# ... agrega test en tests/test_rate_limiting.py ...

# ===== COMMIT =====

# 8. Commitea los cambios
git add src/services/usage_log_service.py tests/test_rate_limiting.py
git commit -m "fix: corrige off-by-one error en rate limiting

- El contador estaba contando un query de más
- Ahora cuenta correctamente los últimos 24 horas
- Agregado test para verificar el fix"

# ===== PUSH =====

# 9. Push a tu fork
git push origin fix/rate-limit-off-by-one

# ===== CREAR PR =====

# 10. Ve a GitHub y crea el PR
# https://github.com/TU_USUARIO/agent-base-project

# 11. Llena la descripción:
# Título: fix: corrige off-by-one error en rate limiting
# Descripción: Explica el problema y la solución

# ===== ESPERAR REVISIÓN =====

# 12. El mantenedor revisa tu código
# Si pide cambios:
git add .
git commit -m "review: responder comentarios"
git push origin fix/rate-limit-off-by-one

# ===== LIMPIAR =====

# 13. Cuando tu PR es mergeado:
git checkout main
git pull origin main
git branch -d fix/rate-limit-off-by-one
git push origin --delete fix/rate-limit-off-by-one
```

---

## 🎯 Guía de Estilo para PRs

### Commits

```bash
# ✅ BIEN
git commit -m "feat: agregar autenticación OAuth

- Implementa login con Google
- Implementa login con GitHub
- Agrega tests para ambos providers"

# ❌ MAL
git commit -m "cambios"
git commit -m "fix stuff"
git commit -m "actualizar archivos"
```

### Código

```python
# ✅ BIEN - Código limpio y documentado
def check_rate_limit(user_id: int) -> RateLimitInfo:
    """
    Verifica si el usuario ha excedido el límite de rate.
    
    Args:
        user_id: ID del usuario
        
    Returns:
        RateLimitInfo con estado actual
        
    Raises:
        RateLimitExceeded: Si se excedió el límite
    """
    # Implementación...

# ❌ MAL - Código sin documentación
def check_rate_limit(user_id):
    # check limit
    pass
```

### Tests

```python
# ✅ BIEN - Tests descriptivos
def test_rate_limit_blocks_after_5_queries():
    """Verifica que el rate limit bloquea después de 5 queries."""
    user = create_test_user()
    
    # Hacer 5 queries
    for i in range(5):
        make_query(user)
    
    # El 6to query debe fallar
    with pytest.raises(RateLimitExceeded):
        make_query(user)

# ❌ MAL - Tests sin descripción
def test_rate_limit():
    user = create_test_user()
    for i in range(5):
        make_query(user)
    with pytest.raises(RateLimitExceeded):
        make_query(user)
```

---

## 🚫 Cosas a Evitar en PRs

### ❌ NO hagas esto

1. **Cambios no relacionados**
   ```bash
   # ❌ MAL: Mezclar bug fix con refactoring
   git commit -m "fix: bug de auth + refactorizar todo el código"
   
   # ✅ BIEN: Cambios separados
   git commit -m "fix: bug de auth"
   # (en otro PR)
   git commit -m "refactor: mejorar estructura del código"
   ```

2. **Commits sin descripción**
   ```bash
   # ❌ MAL
   git commit -m "fix"
   
   # ✅ BIEN
   git commit -m "fix: corrige bug de autenticación en login"
   ```

3. **Cambios de estilo de código**
   ```bash
   # ❌ MAL: Cambiar indentación de todo el archivo
   # ✅ BIEN: Solo cambios necesarios
   ```

4. **Dependencias no necesarias**
   ```bash
   # ❌ MAL: Agregar nuevas dependencias sin justificar
   # ✅ BIEN: Justificar por qué se necesita
   ```

5. **Código sin tests**
   ```bash
   # ❌ MAL: Cambios sin tests
   # ✅ BIEN: Cambios con tests que verifican el fix
   ```

---

## 💬 Comunicación en PRs

### Responder a Comentarios

**Cuando el revisor pide cambios:**

```bash
# 1. Lee el comentario cuidadosamente
# 2. Haz los cambios solicitados
# 3. Commitea con un mensaje claro
git commit -m "review: responder comentario sobre validación de input"

# 4. Push
git push origin tu-rama

# 5. Responde en el comentario del PR
# "Hecho ✅ - He agregado validación adicional como sugeriste"
```

**Ser profesional y respetuoso:**
- ✅ Agradece la revisión
- ✅ Explica tu razonamiento si no estás de acuerdo
- ✅ Sé abierto a sugerencias
- ✅ Mantén un tono positivo

---

## 📊 Ciclo de Vida de un PR

```
1. Crear rama
   ↓
2. Hacer cambios
   ↓
3. Probar localmente
   ↓
4. Push a fork
   ↓
5. Crear PR en GitHub
   ↓
6. Revisor revisa código
   ↓
7. ¿Cambios necesarios?
   ├─ SÍ → Hacer cambios → Volver a paso 6
   └─ NO → Revisor aprueba
   ↓
8. Revisor mergea PR
   ↓
9. Actualizar tu fork
   ↓
10. Limpiar rama local
```

---

## ✅ Checklist Antes de Hacer PR

- [ ] Mi rama está basada en la última versión de upstream/main
- [ ] He probado mi código localmente
- [ ] Todos los tests pasan
- [ ] He agregado tests para mi cambio
- [ ] Mi código sigue el estilo del proyecto
- [ ] He actualizado la documentación si es necesario
- [ ] Mi commit tiene un mensaje descriptivo
- [ ] No hay conflictos con main
- [ ] Mi PR tiene una descripción clara
- [ ] He referenciado issues relacionados
- [ ] He revisado mi propio código antes de enviar

---

## 🎓 Ejemplo Real: PR Completo

### Situación
Encontraste que la documentación de rate limiting tiene un error.

### Solución Completa

```bash
# 1. Actualizar desde upstream
git checkout main
git fetch upstream
git merge upstream/main

# 2. Crear rama
git checkout -b docs/fix-rate-limit-docs

# 3. Editar archivo
# Abres README.md y corriges el error

# 4. Probar (leer la documentación)
# Verificas que la documentación ahora es correcta

# 5. Commit
git add README.md
git commit -m "docs: corrige error en documentación de rate limiting

- El límite era 10/minuto, no 5/24h
- Actualizado con valores correctos
- Agregado ejemplo de uso"

# 6. Push
git push origin docs/fix-rate-limit-docs

# 7. Crear PR en GitHub
# Título: docs: corrige error en documentación de rate limiting
# Descripción:
# ## Problema
# La documentación tenía valores incorrectos del rate limit.
# 
# ## Solución
# Actualicé los valores con los correctos (5 queries/24h).
# 
# ## Testing
# - [x] Leí la documentación actualizada
# - [x] Verificué que es correcta

# 8. Esperar revisión
# El mantenedor revisa y aprueba

# 9. Limpiar
git checkout main
git pull origin main
git branch -d docs/fix-rate-limit-docs
git push origin --delete docs/fix-rate-limit-docs
```

---

## 🎉 ¡Contribuyendo al Proyecto!

Ahora sabes cómo:
- ✅ Hacer fork del proyecto
- ✅ Mantener tu fork actualizado
- ✅ Crear Pull Requests
- ✅ Responder a revisiones
- ✅ Contribuir mejoras al proyecto original

**Beneficios de contribuir:**
- 🌟 Tu código ayuda a otros
- 📚 Mejoras tu experiencia con Git
- 🤝 Te conectas con la comunidad
- 🏆 Tu nombre aparece en el historial del proyecto
- 💡 Recibes feedback de otros desarrolladores

---

## 📚 Recursos Adicionales

- **Git Documentation**: https://git-scm.com/doc
- **GitHub Forking Guide**: https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks
- **Resolving Conflicts**: https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/addressing-merge-conflicts
- **README.md del proyecto**: Documentación completa
- **GETTING_STARTED.md**: Guía para principiantes
- **DEPLOYMENT_GUIDE.md**: Guía de despliegue

---

## 🎉 ¡Listo para Empezar!

Ahora tienes:
- ✅ Tu propio fork del proyecto
- ✅ Configuración de upstream para recibir actualizaciones
- ✅ Proyecto funcionando en local
- ✅ Conocimiento de cómo mantenerlo actualizado

**Ventajas de este workflow:**
- 🔄 Recibes actualizaciones del template
- 📝 Mantienes tu propio historial
- 🎯 Controlas qué cambios aplicar
- 🤝 Puedes contribuir con PRs al original
- 🚀 Independencia total de tu proyecto

**¡Feliz desarrollo!** 💻✨

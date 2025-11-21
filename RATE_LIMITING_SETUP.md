# Rate Limiting para Chatbot - Configuración Completada ✅

## Resumen de Cambios Implementados

Se ha implementado un sistema de **rate limiting de 5 consultas cada 24 horas** para los endpoints de chatbot, utilizando la tabla `UsageLog` existente.

## Archivos Modificados

### 1. `src/core/config.py`
- ✅ Agregadas variables de configuración:
  - `CHATBOT_QUERY_LIMIT = 5`
  - `CHATBOT_QUERY_WINDOW_HOURS = 24`

### 2. `src/services/usage_log_service.py`
- ✅ Agregada función `check_chatbot_rate_limit()` que:
  - Cuenta `main_call_tid` únicos en las últimas 24 horas
  - Retorna: `(puede_consultar, consultas_usadas, consultas_restantes)`
  - Incluye logging para auditoría

### 3. `src/dependencies.py`
- ✅ Agregado dependency `verify_chatbot_rate_limit()` que:
  - Verifica el límite antes de procesar la consulta
  - Retorna HTTP 429 si se excede el límite
  - Incluye headers informativos `X-RateLimit-*`

### 4. `src/routers/chatbot.py`
- ✅ Aplicado rate limiting a:
  - `POST /chatbot/`
  - `POST /chatbot/stream`
- ✅ Reemplazado `get_current_user` por `verify_chatbot_rate_limit`

### 5. `.env.example`
- ✅ Documentadas las nuevas variables de configuración

## 🔧 Configuración Requerida

**IMPORTANTE:** Agrega estas líneas a tu archivo `.env`:

```bash
# Chatbot Rate Limiting
CHATBOT_QUERY_LIMIT=5
CHATBOT_QUERY_WINDOW_HOURS=24
```

## Cómo Funciona

1. **Usuario hace consulta** → Endpoint `/chatbot` o `/chatbot/stream`
2. **Dependency ejecuta** → `verify_chatbot_rate_limit()`
3. **Servicio cuenta** → Consultas únicas por `main_call_tid` en últimas 24h
4. **Si límite OK** → Procesa consulta (se registra automáticamente en `UsageLog`)
5. **Si límite excedido** → Retorna HTTP 429 con detalles

## Respuesta de Error (HTTP 429)

Cuando un usuario excede el límite, recibe:

```json
{
  "detail": {
    "message": "Rate limit exceeded. You have used 5 of 5 queries in the last 24 hours.",
    "queries_used": 5,
    "queries_limit": 5,
    "window_hours": 24,
    "queries_remaining": 0
  }
}
```

**Headers de respuesta:**
```
X-RateLimit-Limit: 5
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 24
```

## Ventajas de Esta Implementación

✅ **Sin nueva tabla** - Usa `UsageLog` existente  
✅ **Sin migraciones** - No requiere cambios en BD  
✅ **Automático** - No necesita registrar manualmente  
✅ **Configurable** - Variables en `.env`  
✅ **Informativo** - Headers y mensajes detallados  
✅ **Auditado** - Logging de cada verificación  

## Testing

### Probar el Rate Limiting

1. Autentícate y obtén un token
2. Haz 5 consultas al endpoint `/chatbot`:
   ```bash
   POST http://localhost:8000/chatbot/
   Authorization: Bearer <tu_token>
   Content-Type: application/json
   
   {
     "message": "Hola"
   }
   ```
3. La 6ta consulta retornará HTTP 429

### Resetear el Límite (para testing)

Opción 1: Espera 24 horas

Opción 2: Elimina registros de `UsageLog` del usuario:
```sql
DELETE FROM usage_logs WHERE user_id = <tu_user_id>;
```

## Personalización

Para cambiar los límites, modifica las variables en `.env`:

```bash
# Ejemplo: 10 consultas cada 12 horas
CHATBOT_QUERY_LIMIT=10
CHATBOT_QUERY_WINDOW_HOURS=12

# Ejemplo: 3 consultas cada 48 horas
CHATBOT_QUERY_LIMIT=3
CHATBOT_QUERY_WINDOW_HOURS=48
```

## Logs

El sistema genera logs informativos:

```
INFO: Chatbot rate limit check for user 1: used=3/5, remaining=2, can_query=True
INFO: Chatbot rate limit check for user 1: used=5/5, remaining=0, can_query=False
```

## Notas Importantes

- ✅ El rate limiting se aplica **por usuario autenticado**
- ✅ Cada consulta al chatbot genera un `main_call_tid` único
- ✅ El conteo es por `main_call_tid` únicos, no por registros totales
- ✅ La ventana de tiempo es deslizante (últimas 24 horas)
- ✅ No afecta otros endpoints, solo `/chatbot` y `/chatbot/stream`

## Próximos Pasos Opcionales

1. **Agregar endpoint de consulta** para que usuarios vean su uso actual:
   ```python
   @router.get("/chatbot/usage")
   async def get_usage(current_user: User = Depends(get_current_user)):
       can_query, used, remaining = check_chatbot_rate_limit(db, current_user.id)
       return {"used": used, "remaining": remaining, "limit": settings.CHATBOT_QUERY_LIMIT}
   ```

2. **Diferentes límites por rol** (usuarios premium vs. free)

3. **Notificaciones** cuando un usuario está cerca del límite

---

**Estado:** ✅ Implementación completada y lista para usar
**Fecha:** 20 de Noviembre, 2025

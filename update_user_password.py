"""
Script para actualizar la contraseña de un usuario específico.

Esto re-hasheará la contraseña con las nuevas rondas de bcrypt (10 rondas).

Uso:
    python update_user_password.py
"""

from sqlalchemy.orm import Session
from src.db.database import SessionLocal
from src.models.user import User
from src.models.profile import Profile  # Importar Profile para evitar error
from src.core.security import hash_password, BCRYPT_ROUNDS
import logging
import time

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def update_user_password(email: str, new_password: str):
    """
    Actualiza la contraseña de un usuario específico.
    
    Args:
        email: Email del usuario
        new_password: Nueva contraseña en texto plano
    """
    db: Session = SessionLocal()
    
    try:
        # Buscar usuario
        user = db.query(User).filter(User.email == email).first()
        
        if not user:
            logger.error(f"❌ Usuario no encontrado: {email}")
            return False
        
        logger.info(f"✅ Usuario encontrado: {user.email} (ID: {user.id})")
        logger.info(f"📊 Rondas de bcrypt configuradas: {BCRYPT_ROUNDS}")
        
        # Hashear nueva contraseña
        logger.info("🔐 Hasheando nueva contraseña...")
        start_time = time.time()
        hashed_password = hash_password(new_password)
        hash_time = time.time() - start_time
        
        logger.info(f"✅ Contraseña hasheada en {hash_time:.3f}s")
        
        # Actualizar contraseña
        user.password = hashed_password
        db.commit()
        
        logger.info(f"✅ Contraseña actualizada exitosamente para {email}")
        logger.info(f"⚡ Ahora el login debería ser ~70% más rápido (~100-150ms)")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Error: {str(e)}")
        db.rollback()
        return False
    finally:
        db.close()


def list_users():
    """Lista todos los usuarios en la base de datos."""
    db: Session = SessionLocal()
    
    try:
        users = db.query(User).all()
        
        if not users:
            logger.warning("⚠️  No hay usuarios en la base de datos")
            logger.info("💡 Crea un usuario con POST /auth/register")
            return
        
        logger.info(f"\n📋 Usuarios en la base de datos ({len(users)}):")
        logger.info("-" * 60)
        for user in users:
            status = "✅ Activo" if user.is_active else "❌ Inactivo"
            logger.info(f"  {user.email}")
            logger.info(f"    ID: {user.id}")
            logger.info(f"    Username: {user.username}")
            logger.info(f"    Estado: {status}")
            logger.info("-" * 60)
        
    except Exception as e:
        logger.error(f"❌ Error: {str(e)}")
    finally:
        db.close()


if __name__ == "__main__":
    logger.info("=" * 80)
    logger.info("🔐 ACTUALIZAR CONTRASEÑA DE USUARIO")
    logger.info("=" * 80)
    
    # Listar usuarios
    list_users()
    
    # Ejemplo de uso
    logger.info("\n💡 Actualizando contraseña de demo1@example.com...")
    
    # Actualizar contraseña del usuario demo1
    update_user_password('demo1@example.com', 'SecurePassword123')

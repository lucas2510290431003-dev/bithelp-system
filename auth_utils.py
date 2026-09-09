"""
Módulo de autenticação segura - Bithelp / GearTech Solutions

Este módulo centraliza o hash e a verificação de senhas usando bcrypt.
Adicione 'bcrypt' ao seu requirements.txt:

"""

import bcrypt


def hash_senha(senha_texto_puro: str) -> str:
    """
    Gera o hash bcrypt de uma senha em texto puro.
    Use isso SEMPRE que for salvar uma senha no banco (cadastro ou alteração).
    """
    senha_bytes = senha_texto_puro.strip().encode("utf-8")
    hash_bytes = bcrypt.hashpw(senha_bytes, bcrypt.gensalt())
    return hash_bytes.decode("utf-8")  # salvar como string no Supabase


def verificar_senha(senha_texto_puro: str, hash_armazenado: str) -> bool:
    """
    Compara uma senha digitada com o hash salvo no banco.
    Retorna True se bater, False caso contrário.
    """
    try:
        senha_bytes = senha_texto_puro.strip().encode("utf-8")
        hash_bytes = hash_armazenado.encode("utf-8")
        return bcrypt.checkpw(senha_bytes, hash_bytes)
    except (ValueError, AttributeError):
        # Acontece se o hash armazenado não for um hash bcrypt válido
        # (ex: durante a transição, se ainda houver senha em texto puro)
        return False
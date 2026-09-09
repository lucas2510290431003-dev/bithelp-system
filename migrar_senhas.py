"""
Script de migração ÚNICA - Bithelp / GearTech Solutions

Converte todas as senhas em texto puro da tabela 'usuarios' para hash bcrypt.

COMO USAR:
1. Rode este script UMA ÚNICA VEZ, antes de colocar o login novo em produção.
2. Depois de rodar, TODAS as senhas no banco viram hash bcrypt.
3. A partir daí, o login (app.py) já deve estar usando verificar_senha()
   em vez de comparar a coluna 'senha' diretamente.
4. Rodar este script duas vezes NÃO quebra nada (ele pula quem já está em hash),
   mas não há necessidade de rodar mais de uma vez.

IMPORTANTE: faça um backup da tabela 'usuarios' no Supabase antes de rodar,
por segurança (Table Editor > usuarios > Export).
"""

import streamlit as st
from supabase import create_client
from auth_utils import hash_senha

# Se for rodar fora do Streamlit (linha de comando), troque estas duas linhas
# por suas credenciais diretamente, ex:
# SUPABASE_URL = "https://xxxx.supabase.co"
# SUPABASE_KEY = "sua_service_role_key_aqui"
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]


def senha_ja_esta_hasheada(valor: str) -> bool:
    """Hashes bcrypt sempre começam com $2b$, $2a$ ou $2y$."""
    return isinstance(valor, str) and valor.startswith(("$2b$", "$2a$", "$2y$"))


def main():
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

    response = supabase.table("usuarios").select("id, nome, senha").execute()
    usuarios = response.data

    if not usuarios:
        print("Nenhum usuário encontrado.")
        return

    migrados = 0
    ja_migrados = 0

    for usuario in usuarios:
        senha_atual = usuario.get("senha", "")

        if senha_ja_esta_hasheada(senha_atual):
            ja_migrados += 1
            continue

        novo_hash = hash_senha(senha_atual)
        supabase.table("usuarios").update({"senha": novo_hash}).eq("id", usuario["id"]).execute()
        migrados += 1
        print(f"✅ Migrado: {usuario['nome']}")

    print("\n--- RESUMO ---")
    print(f"Senhas migradas agora: {migrados}")
    print(f"Já estavam em hash: {ja_migrados}")
    print(f"Total de usuários: {len(usuarios)}")


if __name__ == "__main__":
    main()
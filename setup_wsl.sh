#!/usr/bin/env bash
# =============================================================
# Di cu luan van sang WSL Ubuntu. CHAY BEN TRONG WSL:
#     bash /mnt/d/Master/Thesis/setup_wsl.sh
# Neu bao loi ky tu '\r': chay truoc `sed -i 's/\r$//' /mnt/d/Master/Thesis/setup_wsl.sh`
# =============================================================
set -eo pipefail   # KHONG dung -u: nvm co bien chua gan se lam script chet

SRC="/mnt/d/Master/Thesis"
DST="$HOME/thesis"

echo "==> [1/6] Goi he thong (can sudo)"
sudo apt-get update -y
sudo apt-get install -y curl git python3 python3-venv rsync zstd

echo "==> [2/6] Node.js (LTS) qua nvm"
if [ ! -s "$HOME/.nvm/nvm.sh" ]; then
  curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash
fi
export NVM_DIR="$HOME/.nvm"
# shellcheck disable=SC1091
. "$NVM_DIR/nvm.sh"
nvm install --lts
nvm use --lts
echo "    node $(node -v)"

echo "==> [3/6] Claude Code"
npm install -g @anthropic-ai/claude-code
claude --version || true

echo "==> [4/6] Ollama + model (nomic-embed-text, bge-m3)"
if ! command -v ollama >/dev/null 2>&1; then
  curl -fsSL https://ollama.com/install.sh | sh
fi
# Bat server neu chua chay (WSL khong systemd)
if ! curl -s http://localhost:11434/api/tags >/dev/null 2>&1; then
  nohup ollama serve >/tmp/ollama.log 2>&1 &
  sleep 4
fi
ollama pull nomic-embed-text
ollama pull bge-m3
# Tuy chon (bo dau # neu can dung Qwen VLM mo / LLM-judge llama):
# ollama pull llama3.2
# ollama pull qwen2.5vl:3b
# ollama pull qwen2.5vl:7b

echo "==> [5/6] Copy repo -> $DST"
mkdir -p "$DST"
rsync -a --info=progress2 "$SRC/" "$DST/"

echo "==> [6/6] Python venv + deps trong $DST"
python3 -m venv "$DST/.venv"
"$DST/.venv/bin/pip" install --upgrade pip
"$DST/.venv/bin/pip" install datasets pillow

cat <<EOF

============================================================
XONG. Buoc tiep theo:
  cd $DST
  source .venv/bin/activate     # kich hoat python moi lan lam viec
  claude                        # dang nhap lai tai khoan Claude lan dau

Chay harness (vi du):
  PYTHONIOENCODING=utf-8 python harness/dg1_vh_coverage.py

Ollama: neu WSL cua ban co systemd -> tu chay nen. Neu khong, moi phien
  WSL can bat lai:  ollama serve &   (log o /tmp/ollama.log)
============================================================
EOF

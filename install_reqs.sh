pip install -r requirements.txt
CMAKE_ARGS="-DGGML_CUDA=on" FORCE_CMAKE=1 pip install llama-cpp-python==0.2.88
export HF_HUB_ENABLE_HF_TRANSFER=1
solc-select install all 

apt install postgresql-client postgresql postgresql-contrib -y
apt install -y postgresql-common
/usr/share/postgresql-common/pgdg/apt.postgresql.org.sh 
apt install postgresql-14-pgvector
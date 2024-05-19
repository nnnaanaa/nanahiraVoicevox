import subprocess
import os

def run_docker_compose():
    try:
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        # docker-compose up -dコマンドを実行
        result = subprocess.run(['docker-compose', 'up', '-d'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # 結果の標準出力と標準エラーを取得
        stdout = result.stdout.decode('utf-8')
        stderr = result.stderr.decode('utf-8')

        if stdout:
            print("Standard Output:\n", stdout)
        if stderr:
            print("Standard Error:\n", stderr)
    except subprocess.CalledProcessError as e:
        print("Error occurred while running docker-compose up -d")
        print("Return code:", e.returncode)
        print("Output:", e.output.decode('utf-8'))
        print("Error Output:", e.stderr.decode('utf-8'))

# 関数を呼び出してdocker-composeコマンドを実行
run_docker_compose()

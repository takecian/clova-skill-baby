# coding: utf-8

from flask import Flask, request, jsonify
import os, random
import cek

app = Flask(__name__)

clova = cek.Clova(
    application_id="com.takecian.clova.baby",
    default_language="ja",
    debug_mode=True)


@app.route('/', methods=['GET', 'POST'])
def lambda_handler(event=None, context=None):
    app.logger.info('Lambda function invoked index()')
    return 'hello from Flask!'


# /clova に対してのPOSTリクエストを受け付けるサーバーを立てる
@app.route('/clova', methods=['POST'])
def clova():
    body_dict = clova.route(body=request.data, header=request.headers)
    response = jsonify(body_dict)
    response.headers['Content-Type'] = 'application/json;charset-UTF-8'
    return response


# 起動時の処理
@clova.handle.launch
def launch_request_handler(clova_request):
    open_message = "こんにちは、赤ちゃんをなきやませるよ"
    welcome_japanese = cek.Message(message=open_message, language="ja")
    response = clova.response([welcome_japanese])
    return response


# BabyIntentが解析されたら実行
@clova.handle.intent("BabyIntent")
def send_response(clova_request):
    app.logger.info("Intent started")
    message_japanese = cek.Message(message="泣き止ませるのは任せて！", language="ja")
    response = clova.response([message_japanese])
    return response


# 終了時
@clova.handle.end
def end_handler(clova_request):
    # Session ended, this handler can be used to clean up
    app.logger.info("Session ended.")


# 認識できなかった場合
@clova.handle.default
def default_handler(request):
    return clova.response("理解できませんでした")


if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    app.debug = True
    app.run(host="0.0.0.0", port=port)
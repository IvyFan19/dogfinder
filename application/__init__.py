from flask import Flask, render_template, redirect, request
import requests, json, os

app = Flask(__name__)
base_url = 'https://project3-294022.wl.r.appspot.com'

@app.route('/', methods=['GET'])
def index():    
    test = "result"
    return render_template('index.html', response=test)

# Page: post a dog
@app.route('/post', methods=['GET'])
def post():    
    return render_template('form.html')   

# upload dog info and image
@app.route('/upload', methods =['GET','POST']) 
def upload(): 
    if request.method == 'POST':
        # upload dog image to database
        img_file = request.files.get('file-upload')
        print(img_file)
        post_id = "11111"
        response2 = requests.post(url=base_url+'/api/images/upload/'+post_id, files=img_file)
        
        # test dog image uploaded
        data2 = response2.json()
        status_upload = data2['status']
        image_id = data_upload['image_id']
        print(' * test upload : {}'.format(status_upload))
        print(' * image_id : {}'.format(image_id))

        
        # img_file = request.files.get('file-upload')
        # location = request.form.get('location')
        # email = request.form.get('email')
        # posttype = request.form.get('posttype')
        # print(location, email, posttype, img_file)

        # if not img_file:
        #     return 'No file uploaded.', 400
        # # if not location or email or posttype:
        # #     return "Not complete input", 400

        # # uplaod dog info to database
        # response1 = requests.post(url=base_url+'/api/posts/create', json={
        # 'location': location, 'contact': email, 'post_type': posttype})
        
        # # test dog info uploaded 
        # data1 = response1.json()
        # status1 = data1['status']
        # post_id = data1['post_id']
        # print(' * test 1 : {}'.format(status1))
        # print(' * post_id : {}'.format(post_id))


        
        
    # response1 = requests.post(url=base_url+'/api/posts/create', json={
    #     'location': location, 'contact': email, 'post_type': posttype})
    # # create post test results
    # data1 = response1.json()
    # status1 = data1['status']
    # post_id = data1['post_id']
    # print(' * test 1 : {}'.format(status1))
    # print(' * post_id : {}'.format(post_id))
    # return render_template('index.html', response=data1)  


# @app.route('/doginfo', methods=['GET'])
# def getdoginfo():  
#     ##################################################
#     #                  create new post              #
#     ##################################################
#     response1 = requests.post(url=base_url+'/api/posts/create', json={
#         'location': 'test', 'contact': 'test', 'post_type': 'lost'})

#     # create post test results
#     data1 = response1.json()
#     status1 = data1['status']
#     post_id = data1['post_id']
#     print(' * test 1 : {}'.format(status1))
#     print(' * post_id : {}'.format(post_id))
#     return render_template('post.html', response=data1)  

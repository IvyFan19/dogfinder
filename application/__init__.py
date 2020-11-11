from flask import Flask, render_template, redirect, request, jsonify
import requests, json, os

app = Flask(__name__)
base_url = 'https://project3-294022.wl.r.appspot.com'

@app.route('/', methods=['GET', 'POST'])
def index():  
    if request.method == 'POST':
        term = request.form.get('search_content')
        reponse4 = requests.get(url=base_url+'/api/posts/search/'+term)

        # test search
        data4 = reponse4.json()
        status4 = data4['status']
        results4 = data4['result']
        print(' * * status 4 - search: {}'.format(status4))
        print(' * results 4 : {}'.format(results4))

        return render_template('index.html', entities=results4)

    if request.method == 'GET':
        test = 'get page'
        return render_template('index.html', response=test)
    
# Page: post a dog
@app.route('/post', methods=['GET'])
def post():    
    return render_template('form.html')   

# Upload dog info and image
@app.route('/upload', methods =['GET','POST']) 
def upload(): 
    if request.method == 'POST':
        img_file = request.files.get('file-upload')
        img_name = img_file.filename
        location = request.form.get('location')
        email = request.form.get('email')
        posttype = request.form.get('posttype')
        print(location, email, posttype, img_file)

        if not img_file:
            return 'No file uploaded.', 400
        
        if not (location, email, posttype):
            return 'Not completed form.', 400

        # uplaod dog info to database
        response1 = requests.post(url=base_url+'/api/posts/create', json={
        'location': location, 'contact': email, 'post_type': posttype})
        
        # test dog info uploaded 
        data1 = response1.json()
        status1 = data1['status']
        post_id = data1['post_id']
        print(' * test 1 - upload dog info: {}'.format(status1))
        print(' * * post_id : {}'.format(post_id))

        # upload dog image to database
        content_type = 'image/jpeg'
        file = {'file': (img_name, img_file, content_type)}
        response2 = requests.post(url=base_url+'/api/images/upload/'+post_id, files=file)
        
        # test dog image uploaded
        data2 = response2.json()
        status2 = data2['status']
        image_id = data2['image_id']
        print(' * test 2 - image upload: {}'.format(status2))
        print(' * * image_id : {}'.format(image_id))
        return render_template('index.html')   

# get a dog entity by id
@app.route('/dog/<post_id>', methods=['GET'])
def item(post_id):
    reponse3 = requests.get(url=base_url+'/api/posts/get/'+post_id)
    # get by ID test results
    data3 = reponse3.json()
    status3 = data3['status']
    print(' * test 3 - get dog entity: {}'.format(status3))
    print(' * * dog entity : {}'.format(data3))


       

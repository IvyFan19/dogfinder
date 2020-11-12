from flask import Flask, render_template, redirect, request, jsonify
import requests, json, os
# from flask_googlemaps import GoogleMaps

app = Flask(__name__)
base_url = 'https://project3-294022.wl.r.appspot.com'

# # google api
# app.config['GOOGLEMAPS_KEY'] = "AIzaSyBEEjl88zaaLGz2Q2PWPRm_OxoWG2APJ0k"
# # Initialize the extension
# GoogleMaps(app)

@app.route('/map/<location_str>', methods=['GET', 'POST'])
def map(location_str):
    print(location_str)
    return render_template('map.html', location=location_str)

@app.route('/', methods=['GET', 'POST'])
def index():  
    if request.method == 'POST':
        term = request.form.get('search_content')
        reponse4 = requests.get(url=base_url+'/api/posts/search/'+term)

        # test search
        data4 = reponse4.json()
        status4 = data4['status']
        results4 = data4['result']
        # print(' * * status 4 - search: {}'.format(status4))
        # print(' * results 4 : {}'.format(results4))
        return render_template('index.html', entities=results4)

    if request.method == 'GET':
        reponse5 = requests.get(url=base_url+'/api/posts/search/')

        data5 = reponse5.json()
        status5 = data5['status']
        results5 = data5['result']
        # print(' * * status 5 - list: {}'.format(status5))
        # print(' * results 5 : {}'.format(results5))
        return render_template('index.html', entities=results5)
    
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

        reponse5 = requests.get(url=base_url+'/api/posts/search/')
        data5 = reponse5.json()
        results5 = data5['result']
        return render_template('index.html', entities=results5)   


@app.route('/getid/<post_id>', methods=['GET'])
def getId(post_id):
    print(post_id)
    reponse6 = requests.get(url=base_url+'/api/posts/get/'+post_id)
    data6 = reponse6.json()
    status6 = data6['status']
    result6 = data6['result']
    print(' * test 6 - get 1 dog entity: {}'.format(status6))
    print(' * * dog entity : {}'.format(result6))
    return render_template('edit.html', response=result6)

@app.route('/edit', methods =['GET','POST']) 
def edit():
   
    if request.method == 'POST':
        location = request.form.get('location')
        contact = request.form.get('email')
        posttype = request.form.get('posttype')
        post_id = request.form.get('staticPostId')
        img_file = request.files.get('file-upload')
        image_id = request.form.get('staticImageId')
        print('@@@@@@@@@@@@@@@')
        print("image_id: ", image_id, "post_id: ", post_id, location, contact, posttype)
        
        # edit image 
        if img_file: 
            print("update new image")
            img_name = img_file.filename
            content_type = 'image/jpeg'
            file = {'file': (img_name, img_file, content_type)}
            response = requests.post(url=base_url+'/api/images/upload/'+post_id, files=file)
            reponse_search = requests.get(url=base_url+'/api/posts/search/')
            data = reponse_search.json()
            results = data['result']
            return render_template('index.html', entities=results) 
            
        # keep original image
        else:
            reponse7 = requests.post(url=base_url+'/api/posts/update', json={
            'post_id': post_id, 'image_id': image_id, 'location': location, 
            'contact': contact, 'breed': 'american pit', 'post_type': posttype})
        
            # test edit function
            data7 = reponse7.json()
            status7 = data7['status']
            print(' * test 7 - edit dog entity: {}'.format(status7))

            reponse5 = requests.get(url=base_url+'/api/posts/search/')
            data5 = reponse5.json()
            results5 = data5['result']
            return render_template('index.html', entities=results5) 




       

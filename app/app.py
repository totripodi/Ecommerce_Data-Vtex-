from flask import Flask , render_template , request , jsonify , session
import requests , json

app = Flask(__name__)
app.secret_key= "tomas_dev"

#################LOGIN###########################
@app.route('/',methods=['GET', 'POST'])
def login():
    data={
        "titulo":"  Carga de credenciales",
    } 
    # Si el formulario de inicio de sesión ha sido enviado
    if request.method == 'POST':
        # Obtener los datos del formulario
        account = request.form['account']
        appkey = request.form['appkey']
        apptoken = request.form['apptoken']

        # Comprobar si las credenciales son válidas
        if request_f(account,appkey,apptoken):
            # Guardar las credenciales en la sesión del usuario
            session['account'] = account
            session['appkey'] = appkey
            session['apptoken'] = apptoken

            

    # Obtener los valores de las credenciales guardados en la sesión, si existen
    account = session.get('account')
    print('aca')
    appkey = session.get('appkey')
    apptoken = session.get('apptoken')

    # Mostrar el formulario de inicio de sesión
    return render_template('login.html', data=data,account=account, appkey=appkey, apptoken=apptoken)



   #MENSAJE DE CREDENCIALES Y SELECCION DE OPCION
@app.route("/credenciales", methods=['POST'])
def credenciales():
    
    json_data = request.get_json()

    account_f=json_data['account']
    appkey_f= json_data['appkey']
    apptoken_f= json_data['apptoken']
    
    validacion= request_f(account_f,appkey_f,apptoken_f)
    
    if validacion:
        session['account']=account_f
        session['appkey']=appkey_f
        session['apptoken']=apptoken_f
        respuesta = {
                "result":"ok"
                }
    else:
        respuesta = {
                "result":"error"
                }

    return jsonify(respuesta)
################################MENU#######################################
@app.route('/home',methods=['GET', 'POST'])
def home():
    
    data={
        "titulo":"  Carga de credenciales",
    } 
    
    return render_template('home.html',data=data)


##########################CUSTOMER_QUERY########################
##########################OPCION_1##############################
@app.route('/customer_query', methods=['GET','POST'])
def customer_query():
    account= session['account']
    appkey= session['appkey']
    apptoken= session['apptoken']
    return render_template('customer_query.html',account=account,appkey=appkey,apptoken=apptoken)
  
@app.route('/customer_query_imp', methods=['GET','POST'])
def customer_query_imp():
    email = request.args.get('email')
    print(email)

    account = session['account']
    appkey = session['appkey']
    apptoken = session['apptoken']

    print(account, appkey)
    datos_f = opcion_1(email, account, appkey, apptoken)
    print(datos_f)
    if not any(datos_f):
        datos_f = False
    rendered_template = render_template('opc_1.html', datos_f=datos_f)

    return jsonify({'template': rendered_template})
#funcion_1
def opcion_1(email,account,appkey,apptoken):
    
    email_ing=str(email)
    account=str(account)
    appkey=str(appkey) 
    apptoken=str(apptoken)
    
       
    url = "https://api.vtexcrm.com.br/"+ account +"/dataentities/CL/search?_fields=email,userId,firstName,lastName,isNewsletterOptIn,createdIn,updatedIn,lastInteractionIn&email="+ email_ing
    payload={} 
    headers = {
                'X-VTEX-API-AppKey':appkey,
                'X-VTEX-API-AppToken': apptoken,
                'Cookie': 'janus_sid=181f0575-4fce-4392-bbcb-95bf52b321ba' 
            }
    response = requests.request("GET", url, headers=headers, data=payload)
    json_registros=response.json()
    
    
    #if "email" in json_registros:
    return json_registros
    #else:
     #   vacio="no funciona el request de la opcion 1"
      #  return vacio

#######################VALIDACION DE DATOS########################
def request_f(account_f,AppKey_f,Apptoken_f):
    account_f=str(account_f)
    AppKey_f=str(AppKey_f)
    Apptoken_f=str(Apptoken_f)

    url = "https://api.vtexcrm.com.br/"+ account_f +"/dataentities/CL/search?_fields=email,userId,firstName,lastName,isNewsletterOptIn,createdIn,updatedIn,lastInteractionIn"
    payload={} 
    headers = {
        'X-VTEX-API-AppKey': AppKey_f,
        'X-VTEX-API-AppToken':Apptoken_f,
        'Cookie': 'janus_sid=181f0575-4fce-4392-bbcb-95bf52b321ba'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    if response.status_code == 200:
        return True
    else:
        return False

###########################ORDER_DETAIL_QUERY##########################
###########################OPCION_2##############################
@app.route('/orders_query', methods=['GET','POST'])
def orders_query():           
    account= session['account']
    appkey= session['appkey']
    apptoken= session['apptoken']
    email=""
    ##########Viniendo de customer_query############3
    if len(request.args) > 0:
            email= request.args.get('email') 

    return render_template('orders_query.html',account=account,appkey=appkey,apptoken=apptoken, email=email)
####RESPUESTA_OPC_2######
@app.route('/opc_2', methods=['GET','POST'])
def opc_2():
    account_f= session['account']
    AppKey_f= session['appkey']
    Apptoken_f= session['apptoken']
    email_opc = None 
    email_opc = request.args.get('email_opc')
    

    ##############FECHA#####################
    f_inicial=request.args.get('inicial')
    f_final=request.args.get('final')
    if not f_inicial or not f_final:
        filtrar= 'no'
    else:
        filtrar='si'

    datos=opcion_2(email_opc,account_f,AppKey_f,Apptoken_f,f_inicial,f_final,filtrar)

    rendered_template = render_template('opc_2.html',email_opc=email_opc,f_final=f_final,f_inicial=f_inicial,filtrar=filtrar,datos=datos )
    
    return jsonify({'template': rendered_template})
###FUNCION_2###

def opcion_2(email,account,AppKey,Apptoken,fecha_i,fecha_f,filtrar): #Consulta_datos_órdenes_de_un_cliente
     
    email=str(email)
    
    account=str(account)
    AppKey=str(AppKey)
    Apptoken=str(Apptoken)
    fecha_i=str(fecha_i)
    fecha_f=str(fecha_f)
    filtrar=str(filtrar)    
  

    url = "https://"+account+".vtexcommercestable.com.br/api/oms/pvt/orders?q="+email
    print(url)

    if filtrar=='si':
        str_fechas="f_creationDate=creationDate:["+fecha_i+"T02:00:00.000Z TO "+fecha_f+"T01:59:59.999Z]"
        url= url +"&"+ str_fechas
        
    payload={}
    headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/vnd.vtex.ds.v10+json',
    'X-VTEX-API-AppKey': AppKey,
    'X-VTEX-API-AppToken': Apptoken,
    'Cookie': 'janus_sid=40479b95-c535-4837-906c-22bfd93eb2c8'}

    response = requests.request("GET", url, headers=headers, data=payload)
    json_registros=response.json()

    #print(json_registros)
    
    return json_registros
    
    
#OrderId, OrderNumber, OrderDate, Status
###############################OPCION_3##############################
@app.route('/orders_detail_query', methods=['GET','POST'])
def orders_detail_query():
#############################Viniendo de opcion 2#########################
    orderId=""
    if len(request.args) > 0:
        # Hay una query string en la URL
        orderId = request.args.get('q')      
    
    
    return render_template('/orders_detail_query.html',orderId=orderId)
#######RESPUESTA_DETAIL######
@app.route('/opc_3', methods=['GET','POST'])
def opc_3():
    account_f= session['account']
    AppKey_f= session['appkey']
    Apptoken_f= session['apptoken']
    
    o_id = request.args.get('orderId') 
    data=opcion_3(account_f, AppKey_f, Apptoken_f,o_id)
    if "items" not in data:
        return {"error": "No se encontraron items en la respuesta de la API"}
    for i in data["items"]:
        price=i["price"]
        listprice=i["listPrice"]
    
    value=data["value"]
    formatted_listprice = "${:}".format(listprice/100)
    formatted_price = "${:}".format(price/100)
    formatted_value = "${:}".format(value/100)
    rendered_template = render_template('opc_3.html',data=data,formatted_value=formatted_value,formatted_listprice=formatted_listprice,formatted_price=formatted_price)
    
    return jsonify({'template': rendered_template})
######FUNCION_1####
def opcion_3(account,AppKey,Apptoken,order_id):

    order_id=str(order_id)
    account=str(account)
    url = "https://"+account+".vtexcommercestable.com.br/api/oms/pvt/orders/"+ order_id

    payload={}
    headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/vnd.vtex.ds.v10+json',
    'X-VTEX-API-AppKey': AppKey,
    'X-VTEX-API-AppToken': Apptoken,
    'Cookie': 'janus_sid=b9c6d46d-9b6b-4d29-88c6-e01a5d3d4c1e'
    }

    response =requests.request("GET", url, headers=headers, data=payload)
        
    json_r = response.json()

    return json_r
       
@app.route('/product_search', methods=['GET','POST'])
def product_search():
    search=""
     
    
    return render_template('/product_search.html',search=search)

@app.route('/opc_4', methods=['GET','POST'])
def opc_4():
    search = request.args.get('search')
    
    account= session['account']
    appkey= session['appkey']
    apptoken= session['apptoken']
    data=opcion_4(search,account,appkey,apptoken)
    
    rendered_template = render_template('opc_4.html',data=data)
    
    return jsonify({'template': rendered_template})
    #return render_template('opc_4.html',data=data)


def opcion_4(search,account,appkey,apptoken):
    search=str(search)
    account=str(account)
    appkey=str (appkey)
    apptoken=str(apptoken)
    
    

    url = "https://"+account+".vtexcommercestable.com.br/api/catalog_system/pub/products/search/"+search

    payload={}
    headers = {
    'X-VTEX-API-AppKey': appkey,
    'X-VTEX-API-AppToken': apptoken
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    json_r = response.json()

    
    return json_r


@app.route('/detail_product', methods=['GET','POST'])
def detail_product():
    search= "brazo"
    account= session['account']
    appkey= session['appkey']
    apptoken= session['apptoken']
    data=opcion_4(search,account,appkey,apptoken)

    productId_buscado = request.form['product_id']
    data_json =request.form['data']
    data_j=json.loads(data_json)
    
    print(type(data))
    print(type(data_j))
    
    

    detail=buscar_por_product_id(data,productId_buscado)

    return render_template('detail_product.html',detail=detail)
    

    

def buscar_por_product_id(lista_de_diccionarios, productId_buscado):

    #productId_buscado=str(productId_buscado)
    diccionario_encontrado = None

    for i in lista_de_diccionarios:
        if i["productId"] == productId_buscado:
            print("encontrado")
            diccionario_encontrado = i
            break
    return diccionario_encontrado 
    


if __name__=="__main__":
    app.run(debug=True) 
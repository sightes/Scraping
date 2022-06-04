def easy(producto,maxpage):
    import pandas as pd 
    import numpy as np
    from datetime import date, datetime, timedelta
    import lxml.html
    import json
    import requests 
    producto=producto.replace(' ','%20')
    from requests.packages.urllib3.exceptions import InsecureRequestWarning
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    tabla=[]
    npage=1
    ctabla=[[1]]
    stop=0
    while (len(ctabla)>0 and stop==0):
        print('pagina:' + str(npage))
        url='https://www.easy.cl/'+producto+'?_q=+producto+&layout=list&map=ft&page='+str(npage)
        session=requests.Session()
        session.verify=False
        r = session.get( url.replace(' ',''), headers={
        'Upgrade-Insecure-Requests': '1',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded', \
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36'} )
        root = lxml.html.fromstring(r.text)
        a=root.xpath("////*/template[@data-varname='__STATE__']/script")[0].text
        import json
        y = json.loads(a)
        z=str(y.keys()).replace('dict_keys(','').replace(")'","").replace("["," ").replace("'","").split(',')
        z=pd.DataFrame(z)
        c=z[0].map(lambda x: x[1:12]).values
        c=np.where(np.isin(c,['Product:sp-']))
        z=z.iloc[c]
        c=z[0].map(lambda x: len(x)).values
        c=np.where(c<=20)
        z=z.iloc[c]
        z=z[0].map(lambda x: x[1::])
        z=np.unique(z.values)
        def precio_easy(a):
            url='https://www.easy.cl/'+ a
            r = session.get( url.replace(' ',''), headers={
            'Upgrade-Insecure-Requests': '1',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded', \
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36'} )
            root = lxml.html.fromstring(r.text)
            precio=root.xpath("////*/meta[@property='product:price:amount']/@content")[0]
            imagen=root.xpath("////*/meta[@property='og:image']/@content")[0]
            return(precio,imagen)
        ctabla=[]
        npage=npage+1
        if maxpage>=npage:
            stop=0
        else:
            stop=1
        for n in range(0,len(z)):
            productId=y[z[n]]['productId']
            productName=y[z[n]]['productName']
            brand=y[z[n]]['brand']
            categoryId=y[z[n]]['categoryId']
            productReference=y[z[n]]['productReference']
            productName=y[z[n]]['productName']
            precio,imagen=precio_easy(y[z[n]]['link'])
            ctabla=ctabla+[[productId,productName,brand,categoryId,productReference,precio,imagen]]
        tabla=tabla+ctabla
    return(pd.DataFrame(tabla, columns=['productId','productName','brand','categoryId', \
    'productReference','precio','imagen']))

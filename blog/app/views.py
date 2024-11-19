from django.shortcuts import render, HttpResponse, redirect
from .models import User, Blog, Comment, Like, Category, Product, Order
from django.core.files.storage import FileSystemStorage

def index(requst):
    news = Blog.objects.all()
    print(news)
    return render(requst, 'index.html',{'news': news})


def about(requst):
    return render(requst, 'about.html')


def contacts(requst):
    return render(requst, 'contacts.html')



def reg(requst):
    suc = ''
    if 'user' in requst.session:
        return redirect('/auth')
    if requst.method == 'POST':
        #принимаем данные из формы
        login = requst.POST['login']
        email = requst.POST['email']
        password = requst.POST['password']

        #добавляем данные в модель (базу данных)
        user = User()
        user.login = login
        user.email = email
        user.password = password
        user.save()
        suc = 'Вы успешно зарегистрированы!'
    return render(requst, 'reg.html', {'suc':suc})

def auth(requst):
    user = None
    if requst.method == 'POST':
        #принимаем данные из формы
        login = requst.POST['login']
        password = requst.POST['password']
        if User.objects.filter(login=login).filter(password=password).exists():
            requst.session['user'] = login
    user_blog = []
    orders = None
    if 'user' in requst.session:
        user = User.objects.filter(login=requst.session['user']).first()
        user_blog = Blog.objects.filter(user = user)
        orders = Order.objects.filter(user=user)

    return render(requst, 'auth.html', {'user_blog': user_blog, 'orders': orders, 'user':user})


def logout(request):
    if 'user' in request.session:
        del request.session['user']
    return redirect('/auth')



def add_blog(request):
    user = User.objects.filter(login=request.session['user']).first()
    title = request.POST['title']
    description = request.POST['description']
    full_text = request.POST['full_text']
    path = ''
    if 'image' in request.FILES:
        image = request.FILES['image']
        fs = FileSystemStorage()
        fs.save('blogs/' + image.name, image)
        path = 'blogs/'+image.name

    blog = Blog()
    blog.title = title
    blog.description = description
    blog.full_text = full_text
    blog.user = user
    if path != '':
        blog.image = path
    blog.save()
    return redirect('/')

def view_new(request, id):
    blog_object = Blog.objects.filter(id=id).first()
    blog_object.view += 1
    blog_object.save()

    like_count = 0
    if Like.objects.filter(blog=blog_object).exists():
        like_count = Like.objects.filter(blog=blog_object).first().view

    if request.method == 'POST':
        login = request.POST['login']
        comment = request.POST['comment']

        user_object = User.objects.filter(login=login).first()

        c = Comment()
        c.blog = blog_object
        c.user = user_object
        c.comment = comment
        c.save()
    comments = Comment.objects.filter(blog=blog_object)
    new = Blog.objects.filter(id=id).first()
    return render(request, 'view_new.html', {'new': new, 'comments': comments, 'like_count': like_count})


def add_like(request, id_new):
    user_object = User.objects.filter(login=request.session['user']).first()
    blog_object = Blog.objects.filter(id=int(id_new)).first()
    if Like.objects.filter(blog=blog_object).exists():
        like = Like.objects.filter(blog=blog_object).first()
        like.view += 1
        like.save()
    else:
        l_add = Like()
        l_add.view = 0
        l_add.blog = blog_object
        l_add.user = user_object
        l_add.save()
    return redirect(f'/view/{id_new}')


def catalog(request):
    category = Category.objects.all()
    #products = Product.objects.all()
    return render(request, 'shop/catalog.html', {'category': category})


def catalog_detail(request, id):
    category = Category.objects.filter(id=id).first()
    products = Product.objects.filter(category=category)
    categorys = Category.objects.all()
    return render(request, 'shop/products.html', {'products': products, 'categorys': categorys})

def add_cart(request, id_product):

    if 'cart' in request.session:

        request.session['cart'] += f',{id_product}'
    else:
        request.session['cart'] = str(id_product)
    return redirect('/catalog')

def cart(request):


    products_cart = []
    total_price = 0
    if 'cart' in request.session:
        cart_1 = str(request.session['cart'])
        cart_new = cart_1.split(',')
        f = {}
        for i in cart_new:
            if i in f:
                f[i] += 1
            else:
                f[i] = 1

        for id_product, count_product in f.items():
            if id_product == '':
                continue
            product = Product.objects.filter(id=int(id_product)).first()
            products_cart.append({'id': product.id, 'name': product.name, 'img': product.image, 'price': product.price, 'count': count_product, 'summa': product.price * count_product})
            total_price += count_product * product.price
    cart_bool = False
    if len(products_cart) == 0:
        cart_bool = True

    products_cart = sorted(products_cart, key=lambda p: p['count'], reverse=True)
    return render(request, 'shop/cart.html', {'products_cart': products_cart, 'cart_bool': cart_bool, 'total_price': total_price})

def delete_product(request):
    id_product = request.POST['id_product']
    if 'cart' in request.session:
        id_products = str(request.session['cart']).split(',')
        s = ''
        index = 0
        for id_pr in id_products:
            if id_pr != id_product:
                if index == 0:
                    s += f'{id_pr}'
                else:
                    s += f',{id_pr}'
            index += 1
        request.session['cart'] = s
    return redirect('/cart')

def add_order(request):
    summa = request.POST['summa']
    user = User.objects.filter(login=request.session['user']).first()
    order = Order()
    order.summa = int(summa)
    order.user = user
    order.status = 'Оформлен'
    order.save()
    del request.session['cart']
    return redirect('/auth')
import matplotlib.pyplot as plt
import pandas as pd
import random
import xhtml2pdf.pisa as pisa
from csv import DictReader
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render as render, redirect
from django.template.loader import get_template
from django.views.generic import View
from io import BytesIO
from sklearn.linear_model import LinearRegression

from tvs import models as models
# class to return data for visual
from tvs.datatype import PtrDetails, UserStatusDetail, ToMap1
from tvs.models import Users
from .forms import UserForm, CVUpload, UserMoreInfo, UploadData


# Create your views here.
class ChartData(object):
    @staticmethod
    def check_valve_data():
        data = {'region': [], 'enrolment': [],
                'teacher': [], 'ptr': []}

        values = models.ToChart.objects.all()

        for unit in values:
            data['region'].append(unit.region)
            data['enrolment'].append(unit.enrolment)
            data['teacher'].append(unit.teacher)
            data['ptr'].append(unit.ptr)

        return data


# class to check the highest ptr
class Ptr(object):
    @staticmethod
    def check_ptr():
        module_data = models.ToChart.objects.all()

        check = []

        for i in module_data:

            if float(i.ptr) > 50:
                # data = PtrDetails(i.region, i.ptr)
                data = PtrDetails(i.region, i.ptr)
                check.append(data)
        return check


class MapTz(object):
    @staticmethod
    def cross_check_map():
        filter_ptr = Ptr.check_ptr()
        patch_data_map = []
        for i in filter_ptr:
            if i.region == 'DODOMA':
                i.region = 'tz-do'
            elif i.region == 'GEITA':
                i.region = 'tz-ge'
            elif i.region == 'KATAVI':
                i.region = 'tz-ka'
            elif i.region == 'KIGOMA':
                i.region = 'tz-km'
            elif i.region == 'MARA':
                i.region = 'tz-ma'
            elif i.region == 'RUKWA':
                i.region = 'tz-rk'
            elif i.region == 'SHINYANGA':
                i.region = 'tz-sh'
            elif i.region == 'SIMIYU':
                i.region = 'tz-si'
            elif i.region == 'SINGIDA':
                i.region = 'tz-sd'
            elif i.region == 'SONGWE':
                i.region = 'nill'
            elif i.region == 'TABORA':
                i.region = 'tz-tb'
            elif i.region == 'MOROGORO':
                i.region = 'tz-mo'
            elif i.region == 'MWANZA':
                i.region = 'tz-mw'
            elif i.region == 'KAGERA':
                i.region = 'tz-kr'
            elif i.region == 'ARUSHA':
                i.region = 'tz-as'
            elif i.region == 'MANYARA':
                i.region = 'tz-my'
            elif i.region == 'KILIMANJARO':
                i.region = 'tz-kl'
            elif i.region == 'TANGA':
                i.region = 'tz-tn'
            elif i.region == 'PWANI':
                i.region = 'tz-pw'
            elif i.region == 'DAR ES SALAAM':
                i.region = 'tz-ds'
            elif i.region == 'LINDI':
                i.region = 'tz-li'
            elif i.region == 'MTWARA':
                i.region = 'tz-mt'
            elif i.region == 'RUVUMA':
                i.region = 'tz-rv'
            elif i.region == 'NJOMBE':
                i.region = 'tz-nj'
            elif i.region == 'MBEYA':
                i.region = 'tz-mb'
            elif i.region == 'IRINGA':
                i.region = 'tz-ir'

            pair_data_map = [i.region, float(i.ptr)]
            data_map = ToMap1(pair_data_map)
            patch_data_map.append(data_map)
        return patch_data_map


def index(request, chartID='container', chart_type='column', chart_height=600):
    # load prediction
    predict = PTRDataPrediction()
    prediction = predict.estimatePrediction()

    user = models.User.objects.all().count()
    volunteer = models.Volunteer.objects.all().count()

    global x, y, z
    data = ChartData.check_valve_data()

    teach = data['teacher']
    enrol = data['enrolment']
    ptr = data['ptr']
    region = data['region']

    filter_ptr = Ptr.check_ptr()
    filter_map = MapTz.cross_check_map()

    # iterate the list string parse to float
    teach_data = []
    enrol_data = []
    ptr_data = []
    for x in teach:
        y = float(x)
        teach_data.append(y)

    for x in enrol:
        y = float(x)
        enrol_data.append(y)

    for x in ptr:
        y = float(x)
        ptr_data.append(y)

    chart = {"renderTo": chartID, "type": chart_type, "height": chart_height, }
    title = {"text": 'PTR Government school'}
    xAxis = {"title": {"text": 'Region'}, "categories": region}
    yAxis = {"title": {"text": 'Data'}}

    series = [
        {
            "name": 'Teacher',
            "data": teach_data
        }, {
            "name": 'Enrolment',
            "data": enrol_data
        }, {
            "name": 'PTR(Pupil to Teacher Ratio)',
            "data": ptr_data
        }
    ]

    # print(filter_ptr)
    # print(filter_map)
    # pair the data for the map needs
    multiple_pair = []
    for i in filter_map:
        multiple_pair.append(i.data_pair)

    # pass the context
    to_html = {
        'chartID': chartID, 'chart': chart,
        'series': series, 'title': title,
        'xAxis': xAxis, 'yAxis': yAxis,
        'ptr': ptr_data, 'value': filter_ptr,
        'sample': multiple_pair,
        'predict': int(prediction),
        'user_no': user,
        'volunteer_no': volunteer
    }

    return render(request, template_name='index.html', context=to_html)


@login_required
def home(request, chartID='container', chart_type='column', chart_height=600):
    global x, y, z
    data = ChartData.check_valve_data()

    user = models.User.objects.all().count()
    volunteer = models.Volunteer.objects.all().count()

    # load prediction
    predict = PTRDataPrediction()
    prediction = predict.estimatePrediction()

    # username
    username = request.user.username

    teach = data['teacher']
    enrol = data['enrolment']
    ptr = data['ptr']
    region = data['region']

    filter_ptr = Ptr.check_ptr()
    filter_map = MapTz.cross_check_map()

    # iterate the list string parse to float
    teach_data = []
    enrol_data = []
    ptr_data = []
    for x in teach:
        y = float(x)
        teach_data.append(y)

    for x in enrol:
        y = float(x)
        enrol_data.append(y)

    for x in ptr:
        y = float(x)
        ptr_data.append(y)

    chart = {"renderTo": chartID, "type": chart_type, "height": chart_height, }
    title = {"text": 'PTR Government school'}
    xAxis = {"title": {"text": 'Region'}, "categories": region}
    yAxis = {"title": {"text": 'Data'}}

    series = [
        {
            "name": 'Teacher',
            "data": teach_data
        }, {
            "name": 'Enrolment',
            "data": enrol_data
        }, {
            "name": 'PTR(Pupil to Teacher Ratio)',
            "data": ptr_data
        }
    ]

    # print(filter_ptr)
    # print(filter_map)
    # pair the data for the map needs
    multiple_pair = []
    for i in filter_map:
        multiple_pair.append(i.data_pair)

    # pass the context
    to_html = {
        'chartID': chartID, 'chart': chart,
        'series': series, 'title': title,
        'xAxis': xAxis, 'yAxis': yAxis,
        'ptr': ptr_data, 'value': filter_ptr,
        'sample': multiple_pair,
        'username': username,
        'predict': int(prediction),
        'user_no': user,
        'volunteer_no': volunteer
    }

    return render(request, template_name='home.html', context=to_html)


class ProfileView(View):
    def get(self, request):
        ##loop through the user data
        user_id = request.user.id
        global name, firstname, lastname, email, home, phone, role
        data = models.User.objects.all()
        data1 = models.Users.objects.get(user=user_id)
        username = request.user.username
        for i in data:
            if i.username == username:
                name = username
                firstname = i.first_name
                lastname = i.last_name
                email = i.email
                home = data1.home_address
                phone = data1.phone_number
                role = data1.role

        to_html = {
            'name': name,
            'firstname': firstname,
            'lastname': lastname,
            'email': email,
            'username': username,
            'home': home,
            'phone': phone,
            'role': role,
        }

        return render(request, 'profile.html', context=to_html)

    def post(self, request):
        username = request.user.id
        data = models.Users.objects.get(user=username)
        data1 = models.User.objects.get(username=data.user)
        if request.POST:
            login_data = request.POST.dict()
            firstname = login_data.get("firstname")
            lastname = login_data.get("lastname")
            user_name = login_data.get("username")
            email = login_data.get("email")
            name = login_data.get("home")
            phone = login_data.get("phone")
            data.phone_number = phone
            data.home_address = name
            data1.email = email
            data1.username = user_name
            data1.last_name = lastname
            data1.first_name = firstname
            data.save()
            data1.save()
        return redirect('profile')


def user_status(request):
    value = 0

    voluntee = models.Volunteer.objects.all()
    name = request.user.username

    for i in voluntee:
        if i.username == name:
            value = 1
    return value


# apply.html view
@login_required
def apply(request):
    global to_html, voluntee
    # voluntee = Volunteer()

    voluntee = 0

    name = request.user.username

    int_volunteer_check = user_status(request)

    # print(int_volunteer_check)

    region = AutoSelect.autoselect()

    if request.method == 'POST':
        form = CVUpload(request.POST, request.FILES)
        if int_volunteer_check == 0 or int_volunteer_check is None:

            if form.is_valid():
                if name:
                    # not empty
                    instance = form.save(commit=False)
                    instance.username = name
                    instance.location = region
                    voluntee = voluntee + 1
                    updateChart(voluntee, region)
                    instance.save()
                return redirect('status')
        elif int_volunteer_check == 1:
            form.save(commit=False)
            return redirect('status')
    else:
        form = CVUpload()
        to_html = {
            'data': region,
            'form': form,
            'name': name
        }
    return render(request, 'apply.html', context=to_html)


class Status(object):
    @staticmethod
    def status(request):
        global status_update, location
        name = request.user.username
        voluntee = models.Volunteer.objects.all()
        user_status_info = user_status(request)

        # print(user_status_info)

        detail = []

        if user_status_info == 0 or user_status_info is None:
            status = 'not present, please apply'
            region = 'not allocated'
            length = 'not specified'
            data = UserStatusDetail(status, region, length)
            detail.append(data)
            return detail
        else:
            for i in voluntee:
                if i.username == name:
                    status_update = i.status_update
                    location = i.location

                    period = str(i.length) + ' Months'
                    if i.status_update == 0:
                        change_to = 'Pending approval'
                        data = UserStatusDetail(change_to, i.location, period)
                        detail.append(data)
                    elif i.status_update == 1:
                        change_to = 'Approved'
                        data = UserStatusDetail(change_to, i.location, period)
                        detail.append(data)
                    else:
                        change_to = 'Denied'
                        data = UserStatusDetail(change_to, i.location, period)
                        detail.append(data)
            return detail

            # for i in voluntee:
            #
            #     if user_status_info == 0 or user_status_info is None:
            #         status = 'not present, please apply'
            #         region = 'not allocated'
            #         length = 'not specified'
            #         data = UserStatusDetail(status, region, length)
            #         detail.append(data)
            #     else:
            #         status_update = i.status_update
            #         location = i.location
            #
            #         period = str(i.length) + ' Months'
            #
            #         if i.status_update == 0:
            #             change_to = 'Pending approval'
            #             data = UserStatusDetail(change_to, i.location, period)
            #             detail.append(data)
            #         elif i.status_update == 1:
            #             change_to = 'Approved'
            #             data = UserStatusDetail(change_to, i.location, period)
            #             detail.append(data)
            #         else:
            #             change_to = 'Denied'
            #             data = UserStatusDetail(change_to, i.location, period)
            #             detail.append(data)
            # return detail


@login_required
def status_view(request):
    name = request.user.username
    voluntee_status = Status.status(request)

    to_html = {
        'status': voluntee_status,
        'username': name
    }
    return render(request, template_name='status.html', context=to_html)


# to be finished i.e update chart data
def updateChart(increment, region):
    chartUpdate = models.ToChart.objects.get(region=region)

    old = chartUpdate.teacher
    new = float(old) + float(increment)

    print(str(old))

    print(str(new))

    print(increment)
    print(region)
    # chartUpdate.teacher =


# manage.html view
# approve or disapprove volunteers
@user_passes_test(lambda u: u.is_superuser)
def approveVolunteer(request):
    global fname, to_html
    name = request.user.username
    user_id = request.user.id
    volunteer = models.Volunteer.objects.all()
    files = models.UploadFileCvs.objects.all()

    # queries for all education level
    cert = models.Volunteer.objects.filter(certificate='Certificate level')
    cert1 = models.Volunteer.objects.filter(certificate='Certificate level', status_update=str(1))
    dipl = models.Volunteer.objects.filter(certificate='Diploma level')
    dipl1 = models.Volunteer.objects.filter(certificate='Diploma level', status_update=str(1))
    degr = models.Volunteer.objects.filter(certificate='Degree level')
    degr1 = models.Volunteer.objects.filter(certificate='Degree level', status_update=str(1))
    mast = models.Volunteer.objects.filter(certificate='Masters level')
    mast1 = models.Volunteer.objects.filter(certificate='Masters level', status_update=str(1))

    paginator = Paginator(files, 5)

    page = request.GET.get('page')

    try:
        # create Page object for the given page
        files = paginator.page(page)
    except PageNotAnInteger:
        # if page parameter in the query string is not available, return the first page
        files = paginator.page(1)
    except EmptyPage:
        # if the value of the page parameter exceeds num_pages then return the last page
        files = paginator.page(paginator.num_pages)

    # Get the index of the current page
    index = files.number - 1  # edited to something easier without index
    # This value is maximum index of your pages, so the last page - 1
    max_index = len(paginator.page_range)
    # You want a range of 7, so lets calculate where to slice the list
    start_index = index - 3 if index >= 3 else 0
    end_index = index + 3 if index <= max_index - 3 else max_index
    # Get our new page range. In the latest versions of Django page_range returns
    # an iterator. Thus pass it to list, to make our slice possible again.
    page_range = list(paginator.page_range)[start_index:end_index]

    if request.method == 'POST':
        form = UploadData(request.POST, request.FILES)

        data = request.POST.dict()
        filename = data.get("file-name")

        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            return redirect('clean')

        # clean and upload file
        if str(filename) == "":
            print('empty')
        else:
            file = models.UploadFileCvs.objects.all()
            for i in file:
                if str(filename) == str(i.filename):
                    # print(i.uploadcvs)
                    AutoClean.clean_data(i.uploadcvs)
                    # print(filename)
                    redirect('clean')
            redirect('clean')
        redirect('clean')

    else:
        form = UploadData()
        to_html = {
            'name': volunteer,
            'form': form,
            'file': files,
            'page': page_range,
            'cert': cert,
            'cert1': cert1,
            'dipl': dipl,
            'dipl1': dipl1,
            'degr': degr,
            'degr1': degr1,
            'mast': mast,
            'mast1': mast1
        }

    return render(request, template_name='manage.html', context=to_html)


# autoselect the location for the volunteer
class AutoSelect:
    @staticmethod
    def autoselect():
        filter_ptr = Ptr.check_ptr()
        choices = []

        for i in filter_ptr:
            choices.append(i.region)

        return random.choice(choices)


class UserFormView(View):
    form_class = UserForm

    # form_class_info=UserMoreInfo

    # blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, 'signup-form.html', {'form': form})

    # process form data
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            # clean data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            # return user objects if is valid
            user = authenticate(username=username, password=password)

            if user is not None:

                if user.is_active:
                    login(request, user)
                    user = user.username
                    to_html = {
                        'user': user
                    }
                    # home()
                    return redirect('complete_signup')

        return render(request, 'signup-form.html', {'form': form})


# signup proceed page
class UserCompleteSignUp(View):
    form_class = UserMoreInfo

    # blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, 'complete-signup.html', {'form': form})

    # process form data
    def post(self, request):
        username = request.user
        form = self.form_class(request.POST)

        if form.is_valid():
            home_address = form.cleaned_data['home_address']
            phone_number = form.cleaned_data['phone_number']
            role = form.cleaned_data['role']
            userInfo = Users(user=username, home_address=home_address, phone_number=phone_number, role=role)
            userInfo.save()
            return redirect('home')

        return render(request, 'signup-form.html', {'form': form})


# predict the PTR using linear regression
class PTRDataPrediction:
    # read the file
    def readFile(self):
        filePath = "media/documents/test2.csv"
        data = pd.read_csv(filePath)
        data = data[['REGION', 'PTR']]
        # changing the region name to number for prediction
        data['REGION'] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26]
        return data

    def prediction(self):
        data = self.readFile()
        X = data['REGION'].values.reshape(-1, 1)
        y = data['PTR'].values.reshape(-1, 1)
        reg = LinearRegression()
        reg.fit(X, y)
        predictions = reg.predict(X)
        return predictions

    def plotingGraph(self):
        data = self.readFile()
        predictions = self.prediction()
        plt.figure(figsize=(16, 8))
        plt.scatter(
            data['REGION'],
            data['PTR'],
            c='black'
        )
        plt.plot(
            data['REGION'],
            predictions,
            c='blue',
            linewidth=2
        )
        plt.xlabel("Money spent on TV ads ($)")
        plt.ylabel("Sales ($)")
        # plt.show()

    def estimatePrediction(self):
        predictions = self.prediction()
        total = 0
        for i in predictions:
            for j in i:
                total += j

        sizeOfData = len(predictions)

        estimation = total / sizeOfData

        return estimation


class Render:
    @staticmethod
    def render(path: str, params: dict):
        template = get_template(path)
        html = template.render(params)
        response = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), response)
        if not pdf.err:
            return HttpResponse(response.getvalue(), content_type='application/pdf')
        else:
            return HttpResponse("Error Rendering PDF", status=400)


# preview a pdf plus downloading it
class Pdf(View):
    def get(self, request, full_name):
        global fname, params
        name = models.Users.objects.all()
        name1 = models.User.objects.all()
        volunteer = models.Volunteer.objects.get(full_name=full_name)

        for i in name:
            for j in name1:
                if str(volunteer.username) == str(i.user) == str(j.username):
                    params = {
                        'name': volunteer.full_name,
                        'address': i.home_address,
                        'contact': volunteer.contact,
                        'carrier': volunteer.carrier,
                        'experience': volunteer.experience,
                        'skill': volunteer.skills,
                        'why': volunteer.why_volunteer,
                        'role': i.role,
                        'email': j.email
                    }

        return Render.render('previewPDF.html', params)
        # return render(request,template_name='test.html',context=None)


# auto clean data
class AutoClean:
    @staticmethod
    def clean_data(filepath):
        global new_data, group_data
        path = "media/documents/"

        # var = input("Please enter the file name for data cleaning: ")

        data = pd.read_csv(filepath, encoding='latin1')

        data1 = data[['REGION', 'ENROLMENT', 'ALL TEACHERS', 'PTR']]

        # check if null or missing data
        check_null = data1.isnull().values.any()

        if check_null:
            # data has a null or empty field
            # then interpolate estimates
            new_data = data1.interpolate()
            group_data = new_data.groupby('REGION').mean()
            group_data.to_csv(path + 'test2.csv')
            handle()
        else:
            # data has no null or empty field
            group_data = data1.groupby('REGION').mean()
            group_data.to_csv(path + 'test2.csv')
            handle()


# read, upload, update csv data
def handle():
    global v
    if models.ToChart.objects.exists():
        global row_id, num
        print('data already loaded...exiting.')
        print('updating it')
        # retrieve the data
        row_id = []
        num = 0
        data = models.ToChart.objects.all()
        # loop to append ids for incremental
        for c in data:
            row_id.append(c.id)

        for row in DictReader(open('media/documents/test2.csv')):
            data = models.ToChart.objects.get(id=row_id[num])
            data.region = row['REGION']
            data.enrolment = row['ENROLMENT']
            data.teacher = row['ALL TEACHERS']
            data.ptr = row['PTR']
            data.save()
            num = num + 1
        return
    print("Loading data available")
    for row in DictReader(open('media/documents/test2.csv')):
        data = models.ToChart()
        data.region = row['REGION']
        # data.council = row['COUNCIL']
        # data.ward = row['WARD']
        # data.school = row['SCHOOL NAME']
        data.enrolment = row['ENROLMENT']
        data.teacher = row['ALL TEACHERS']
        data.ptr = row['PTR']
        data.save()


# update user status i.e approve 1 or 0
def updateStatus(request, full_name):
    global data

    num = 1
    num1 = 0

    volunteer = models.Volunteer.objects.get(full_name=full_name)
    v = models.Volunteer.objects.get(id=volunteer.id)
    # name = models.User.objects.get(id=volunteer.id)

    # for i in name:
    # if v.username == request.user.username:
    if v.status_update == 0:
        v.status_update = num
        v.save()
        data = {
            'value': 1
        }
    elif v.status_update == 1:
        v.status_update = num1
        v.save()
        data = {
            'value': 0
        }

    return redirect('manage_applicant', v.certificate)
    # return JsonResponse(data)


# manage specific applicant i.e. certificate, diploma
@user_passes_test(lambda u: u.is_superuser)
def manage_applicant(request, certificate):
    volunteer = models.Volunteer.objects.filter(certificate=certificate).order_by('status_update').all()

    to_html = {
        'applicant': volunteer
    }

    return render(request, template_name='manageApplicant.html', context=to_html)

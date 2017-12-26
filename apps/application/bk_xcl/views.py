#encoding:utf-8
from app import app, db
from flask import render_template, current_app, g, session, request, flash, make_response, send_file, url_for
from flask_login import current_user, login_user, logout_user , login_required
from app.form import *
from werkzeug.security import generate_password_hash, check_password_hash
from flask_principal import Identity, AnonymousIdentity, identity_changed, Permission, RoleNeed
import time
import random

from sqlalchemy import func
from app.utils import *
import platform
config = app.config




admin_permission = Permission(RoleNeed('admin'))
dev_permission = Permission(RoleNeed('dev'))
audit_permission = Permission(RoleNeed('audit'))

@app.before_request
def before_request():
    g.user = current_user

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter(User.name == form.name.data).first()
        if user is not None:
            if check_password_hash(user.hash_pass, form.passwd.data):
                login_user(user)
                identity_changed.send(current_app._get_current_object(),
                                      identity=Identity(user.id))
                return redirect('dashboard')
            else:
                flash(u'密码不正确！')
        else:
            flash(u'用户不存在！')



    return render_template('login.html', form=form)
@app.route('/logout')
@login_required
def logout():
    logout_user()
    for key in ('identity.name', 'identity.auth_type'):
        session.pop(key, None)
    identity_changed.send(current_app._get_current_object(),
                          identity=AnonymousIdentity())
    return redirect('login')
@app.route('/passwd', methods = ['GET', 'POST'])
@login_required
def passwd():
    form = PasswdForm()
    if form.validate_on_submit():
        if form.new_pass.data == form.rep_pass.data:
            if check_password_hash(current_user.hash_pass, form.old_pass.data):
                current_user.hash_pass = generate_password_hash(form.new_pass.data)
                db.session.commit()
                return redirect('dashboard')


    return render_template('passwd.html', form=form)

@app.route('/mysql_db')
@admin_permission.require()
def mysql_db():
    dbconfigs=Dbconfig.query.all()

    return render_template('mysql_db.html',dbconfigs=dbconfigs)
@app.route('/mysql_db/create', methods = ['GET', 'POST'])
@admin_permission.require()
def mysql_db_create():
    form = MysqlDbForm()
    if form.validate_on_submit():
        dbconfig = Dbconfig()
        dbconfig.name = form.name.data
        dbconfig.host = form.host.data
        dbconfig.port = form.port.data
        dbconfig.user = form.user.data
        aes_pass = base64.b64encode(form.password.data)
        dbconfig.password = aes_pass
        db.session.add(dbconfig)
        db.session.commit()
        return redirect('mysql_db')
    return render_template('mysql_db_create.html', form=form)
@app.route('/mysql_db/update/<int:id>', methods = ['GET', 'POST'])
@admin_permission.require()
def mysql_db_update(id):
    dbconfig=Dbconfig.query.get(id)
    form = MysqlDbForm()
    if form.validate_on_submit():
        dbconfig.name = form.name.data
        dbconfig.host = form.host.data
        dbconfig.port = form.port.data
        dbconfig.user = form.user.data
        if form.password.data is not None:
            aes_pass = base64.b64encode(form.password.data)
            dbconfig.password = aes_pass
        dbconfig.update_time = datetime.now()
        db.session.commit()
        return redirect('mysql_db')

    return render_template('mysql_db_update.html', form=form, dbconfig=dbconfig)
@app.route('/mysql_db/delete/<int:id>')
@admin_permission.require()
def mysql_db_delete(id):
    dbconfig = Dbconfig.query.get(id)
    db.session.delete(dbconfig)
    db.session.commit()
    return redirect('mysql_db')

@app.route('/user')
@admin_permission.require()
def user():
    users = User.query.filter(User.role != 'admin')

    return render_template('user.html', users=users)
@app.route('/user/create', methods = ['GET', 'POST'])
@admin_permission.require()
def user_create():
    form = UserForm()
    if form.validate_on_submit():
        user = User()
        user.name = form.name.data
        user.hash_pass = generate_password_hash(form.passwd.data)
        user.role = form.role.data
        user.email = form.email.data
        db.session.add(user)
        db.session.commit()
        return redirect('user')
    return render_template('user_create.html', form=form)
@app.route('/user/update/<int:id>', methods = ['GET', 'POST'])
@admin_permission.require()
def user_update(id):
    user = User.query.get(id)
    form = UserForm()
    if form.validate_on_submit():
        user.hash_pass = generate_password_hash(form.passwd.data)
        user.email = form.email.data
        db.session.commit()
        return redirect('user')
    return render_template('user_update.html', form=form, user=user)
@app.route('/user/delete/<int:id>', methods = ['GET', 'POST'])
@admin_permission.require()
def user_delete(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return redirect('user')
@app.route('/user/srole/<int:id>')
@admin_permission.require()
def user_srole(id):
    user = User.query.get(id)
    if user.srole == 0:
        user.srole = 1
    else:
        user.srole = 0
    db.session.commit()
    return redirect('user')

@app.route('/user/db_alloc/<int:id>', methods = ['GET', 'POST'])
@admin_permission.require()
def user_db_alloc(id):
    user=User.query.get(id)
    userdbconfigs=user.dbs
    alldbconfigs=Dbconfig.query.all()
    for userdbconfig in userdbconfigs:
        if userdbconfig in alldbconfigs:
            alldbconfigs.remove(userdbconfig)
    form = UserDbForm()
    if form.validate_on_submit():
        dbconfig=Dbconfig.query.get(form.db.data)
        user.dbs.append(dbconfig)
        db.session.commit()
        return redirect(url_for('user_db_alloc', id=id))

    return render_template('user_db_alloc.html', form=form, user=user, userdbconfigs=userdbconfigs, alldbconfigs=alldbconfigs)
@app.route('/user/db_delete/<int:userid><int:dbid>')
@admin_permission.require()
def user_db_delete(userid,dbid):
    user = User.query.get(userid)
    dbconfig = Dbconfig.query.get(dbid)
    user.dbs.remove(dbconfig)
    db.session.commit()
    return redirect(url_for('user_db_alloc', id=userid))


@app.route('/admin_chart/<int:days>')
@admin_permission.require()
def admin_chart(days=7):
    dayrange=[]
    today = date.today()
    dayrange.append(str(today))
    for day in range(1,days):
        datetmp = today-timedelta(days=day)
        dayrange.append(str(datetmp))
    dayrange.sort()

    daycounts=[]
    for i in range(len(dayrange)):
        daycount=Work.query.filter(Work.create_time.like(dayrange[i]+'%')).count()
        daycounts.append(daycount)
    dayago = today-timedelta(days=days)

    works = db.session.query(Work.status).filter(Work.create_time >= dayago)

    workstatus={u'正常结束':0, u'待人工审核':0, u'自动审核失败':0, u'执行中':0, u'执行异常':0, u'开发人中止':0, u'审核人中止':0, u'管理员中止':0, u'审核人驳回':0}
    for work in works:
        if work.status == 0:
            workstatus[u'正常结束']+=1
        elif work.status == 1:
            workstatus[u'待人工审核']+=1
        elif work.status == 2:
            workstatus[u'自动审核失败']+=1
        elif work.status == 3:
            workstatus[u'执行中'] += 1
        elif work.status == 4:
            workstatus[u'执行异常']+=1
        elif work.status == 5:
            workstatus[u'开发人中止']+=1
        elif work.status == 6:
            workstatus[u'审核人中止']+=1
        elif work.status == 7:
            workstatus[u'管理员中止']+=1
        elif work.status == 8:
            workstatus[u'审核人驳回']+=1

    dev_dist = db.session.query(Work.dev.label('dev'),
                                func.count(Work.dev).label('count')).filter(Work.create_time >= dayago).group_by(Work.dev)
    audit_dist = db.session.query(Work.audit.label('audit'),
                                func.count(Work.dev).label('count')).filter(Work.create_time >= dayago).group_by(Work.audit)


    return render_template('admin_chart.html',dayrange=dayrange, daycounts=daycounts, workstatus=workstatus, dev_dist=dev_dist, audit_dist=audit_dist, days=days)
@app.route('/modules')
@admin_permission.require()
def modules():
    checksqladvisorresult=checksqladvisor()


    return render_template('modules.html',checksqladvisorresult=checksqladvisorresult)
@app.route('/sqladvisor_install')
@admin_permission.require()
def sqladvisor_install():
    release = platform.dist()[0]
    sqladvisor_dir = base_dir + '/sqladvisor'
    if release == 'centos':
        subprocess.Popen('yum install -y http://www.percona.com/downloads/percona-release/redhat/0.1-3/percona-release-0.1-3.noarch.rpm&&yum install -y Percona-Server-shared-56', shell=True)
        time.sleep(10)
        subprocess.Popen('rm -rf SQLAdvisor-master&&yum install -y unzip cmake libaio-devel libffi-devel glib2 glib2-devel&&unzip SQLAdvisor-master.zip&&cd SQLAdvisor-master&&ln -sf /usr/lib64/libperconaserverclient_r.so.18 /usr/lib64/libperconaserverclient_r.so &&cmake -DBUILD_CONFIG=mysql_release -DCMAKE_BUILD_TYPE=debug -DCMAKE_INSTALL_PREFIX=/usr/local/sqlparser ./&&make && make install&&cd sqladvisor&&cmake -DCMAKE_BUILD_TYPE=debug ./&&make&&chmod +x sqladvisor&&cp -rf sqladvisor '+sqladvisor_dir, shell=True)
    elif release == 'ubuntu':
        subprocess.Popen(
            'apt-get install -y http://www.percona.com/downloads/percona-release/redhat/0.1-3/percona-release-0.1-3.noarch.rpm&&apt-get install -y Percona-Server-shared-56',
            shell=True)
        time.sleep(10)
        subprocess.Popen(
            'rm -rf SQLAdvisor-master&&apt-get install -y unzip cmake libaio-devel libffi-devel glib2 glib2-devel&&unzip SQLAdvisor-master.zip&&cd SQLAdvisor-master&&ln -sf /usr/lib64/libperconaserverclient_r.so.18 /usr/lib64/libperconaserverclient_r.so &&cmake -DBUILD_CONFIG=mysql_release -DCMAKE_BUILD_TYPE=debug -DCMAKE_INSTALL_PREFIX=/usr/local/sqlparser ./&&make && make install&&cd sqladvisor&&cmake -DCMAKE_BUILD_TYPE=debug ./&&make&&chmod +x sqladvisor&&cp -rf sqladvisor ' + sqladvisor_dir,
            shell=True)
    time.sleep(180)
    return redirect('modules')
@app.route('/sqladvisor_uninstall')
@admin_permission.require()
def sqladvisor_uninstall():
    sqladvisor_dir = base_dir + '/sqladvisor'
    os.remove(sqladvisor_dir+'/sqladvisor')
    return redirect('modules')


@app.route('/slowlog')
@login_required
def slowlog():
    if current_user.role == 'dev':
        dbconfigs = current_user.dbs
    else:
        dbconfigs = Dbconfig.query.all()

    return render_template('slowlog.html', dbconfigs=dbconfigs)
@app.route('/view_slowlog/<int:dbid>/<int:t>')
@login_required
def view_slowlog(dbid, t=1):
    slowloglist=getSlowLogList(dbid, t)
    dbconfig = Dbconfig.query.get(dbid)

    return render_template('view_slowlog.html', slowloglist=slowloglist, dbconfig=dbconfig)

@app.route('/dbreport/<int:id>', methods = ['GET', 'POST'])
@admin_permission.require()
def dbreport(id):
    dbconfig = Dbconfig.query.get(id)
    dbreports = Report.query.filter(Report.db_name == dbconfig.name)
    form = ReportForm()
    if form.validate_on_submit():
        report = Report()
        report.db_name = dbconfig.name
        report.mem = form.mem.data
        report.create_time = datetime.now()
        report.report_content = getdbReport(id, form.mem.data)
        db.session.add(report)
        db.session.commit()
    return render_template('dbreport.html', form=form, dbconfig=dbconfig, dbreports=dbreports)

@app.route('/dbreport_view/<int:id>')
@admin_permission.require()
def dbreport_view(id):
    dbreport = Report.query.get(id)

    return render_template('dbreport_view.html', dbreport=dbreport)

@app.route('/dbreport_delete/<int:dbid>/<int:id>')
@admin_permission.require()
def dbreport_delete(dbid, id):
    dbreport = Report.query.get(id)
    db.session.delete(dbreport)
    db.session.commit()
    return redirect(url_for('dbreport', id=dbid))





@app.route('/dev_work')
@dev_permission.require()
def dev_work():
    works = Work.query.filter(Work.dev == current_user.name)
    return render_template('dev_work.html', works=works)
@app.route('/dev_work/create', methods = ['GET', 'POST'])
@dev_permission.require()
def dev_work_create():
    db_configs = current_user.dbs
    if config.get('AUDIT_SROLE_ON_OFF') == 'ON':
        audits = User.query.filter(User.role == 'audit', User.srole == 1)
    else:
        audits = User.query.filter(User.role == 'audit', User.srole == 0)
    form = WorkForm()
    if form.validate_on_submit():
        sqlContent=form.sql_content.data
        dbConfig=form.db_config.data
        isBackup=form.backup.data
        sqlContent = sqlContent.rstrip()
        if sqlContent[-1] == ";":
            work = Work()
            if form.name.data:
                work.name = form.name.data
            else:
                work.name = 't_'+current_user.name+'_'+str(int(time.time())) + str(random.randint(0, 9)) + str(random.randint(0, 9)) + str(random.randint(0, 9)) + str(random.randint(0, 9)) + str(random.randint(0, 9)) + str(random.randint(0, 9))
            work.db_config = dbConfig
            work.backup = isBackup
            work.dev = current_user.name
            work.audit = form.audit.data
            audit=User.query.filter(User.name == work.audit).first()
            work.srole = audit.srole
            work.sql_content = sqlContent

            result = sqlautoReview(sqlContent, dbConfig, isBackup)
            if result or len(result) != 0:
                jsonResult = json.dumps(result)
                work.status = 1
                for row in result:
                    if row[2] == 2:
                        work.status = 2
                        break
                    elif re.match(r"\w*comments\w*", row[4]):
                        work.status = 2
                        break
                work.auto_review = jsonResult
                work.create_time = datetime.now()

                db.session.add(work)
                db.session.commit()

                if mailonoff == 'ON':
                    audit=User.query.filter(User.name == work.audit).first()
                    send_email(u'【inception_web】新工单通知',u'您好，你有一条新的工单（'+work.name+u'），请审核，谢谢！',audit.email)
                return redirect('dev_work')
            else:
                flash('inception返回的结果集为空！可能是SQL语句有语法错误!')
        else:
            flash(u'SQL语句结尾没有以;结尾，请重新修改并提交！')

    return render_template('dev_work_create.html', form=form, db_configs=db_configs, audits=audits)
@app.route('/dev_work/update/<int:id>', methods = ['GET', 'POST'])
@dev_permission.require()
def dev_work_update(id):
    work=Work.query.get(id)
    db_configs = current_user.dbs
    audits = User.query.filter(User.role == 'audit')
    form = WorkForm()
    if form.validate_on_submit():
        sqlContent = form.sql_content.data.rstrip()
        if sqlContent[-1] == ";":
            result = sqlautoReview(sqlContent, work.db_config, work.backup)
            if result or len(result) != 0:
                jsonResult = json.dumps(result)
                work.status = 1
                for row in result:
                    if row[2] == 2:
                        work.status = 2
                        break
                    elif re.match(r"\w*comments\w*", row[4]):
                        work.status = 2
                        break
                work.auto_review = jsonResult
                work.sql_content = sqlContent
                db.session.commit()


                if mailonoff == 'ON':
                    audit = User.query.filter(User.name == work.audit).first()
                    send_email(u'【inception_web】修改工单通知', u'您好，你有一条刚修改的工单（' + work.name + u'），请审核，谢谢！', audit.email)
                return redirect('dev_work')
            else:
                flash('inception返回的结果集为空！可能是SQL语句有语法错误!')
        else:
            flash(u'SQL语句结尾没有以;结尾，请重新修改并提交！')
    return render_template('dev_work_update.html', form=form, db_configs=db_configs, audits=audits, work=work)
@app.route('/dev_work/delete/<int:id>', methods = ['GET', 'POST'])
@dev_permission.require()
def dev_work_delete(id):
    work = Work.query.get(id)
    db.session.delete(work)
    db.session.commit()
    return redirect('dev_work')


@app.route('/dev_work/check', methods = ['POST'])
@dev_permission.require()
def dev_work_check():
    data = request.form
    sqlContent=data['sqlContent']
    dbConfig=data['dbConfig']
    finalResult = {'status': 0, 'msg': 'ok', 'data': []}
    if not sqlContent or not dbConfig:
        finalResult['status'] = 1
        finalResult['msg'] = '数据库或SQL内容可能为空'
        return json.dumps(finalResult)
    sqlContent = sqlContent.rstrip()
    if sqlContent[-1] != ";":
        finalResult['status'] = 2
        finalResult['msg'] = 'SQL语句结尾没有以;结尾，请重新修改并提交！'
        return json.dumps(finalResult)
    result = sqlautoReview(sqlContent, dbConfig)
    if result is None or len(result) == 0:
        finalResult['status'] = 3
        finalResult['msg'] = 'inception返回的结果集为空！可能是SQL语句有语法错误'
        return json.dumps(finalResult)
    finalResult['data'] = result
    return json.dumps(finalResult)

@app.route('/list_db', methods = ['POST'])
@dev_permission.require()
def list_db():
    listdb=[]
    data = request.form
    dbConfigName = data['dbConfig']
    if dbConfigName:
        listdb = getAlldbByDbconfig(dbConfigName)
    return json.dumps(listdb)

#add by xucl for rollback
@app.route('/list_binlog', methods = ['POST'])
#@dev_permission.require()
def list_binlog():
    listbinlog=[]
    data = request.form
    dbConfigName = data['dbConfig']
    if dbConfigName:
        listbinlog = getAllbinlogfile(dbConfigName)
    return json.dumps(listbinlog)


@app.route('/sqladvisor_check', methods = ['GET', 'POST'])
@dev_permission.require()
def sqladvisor_check():
    if request.method == 'POST':
        data = request.form
        dbConfig = data['dbConfig']
        dbUse = data['dbUse']
        sqlContent = data['sqlContent']
        sqlContent = sqlContent.rstrip()
        sqlContent = sqlContent.replace('\n', '')
        sqlList = sqlContent.split(';')

        sqlList.reverse()
        sqlResult={}
        for sqldata in sqlList:
            if sqldata:
                sqldata
                sqlResult.setdefault(sqldata)
                result= mysqladvisorcheck(sqldata, dbConfig, dbUse)
                result = result.split('\n\n')
                sqlResult[sqldata] = result
        return json.dumps(sqlResult)
    dbconfigs=current_user.dbs
    return render_template('sqladvisor_check.html', dbconfigs=dbconfigs)

@app.route('/rollback', methods = ['GET', 'POST'])
@dev_permission.require()
def rollback():
    if request.method == 'POST':
        data = request.form
        dbConfig = data['dbConfig']
        dbUse = data['dbUse']
        sqlContent = data['sqlContent']
        sqlContent = sqlContent.rstrip()
        sqlContent = sqlContent.replace('\n', '')
        sqlList = sqlContent.split(';')

        sqlList.reverse()
        sqlResult={}
        for sqldata in sqlList:
            if sqldata:
                sqldata
                sqlResult.setdefault(sqldata)
                result= mysqladvisorcheck(sqldata, dbConfig, dbUse)
                result = result.split('\n\n')
                sqlResult[sqldata] = result
        return json.dumps(sqlResult)
    dbconfigs=current_user.dbs
    return render_template('rollback.html', dbconfigs=dbconfigs)


@app.route('/dev_chart/<int:days>')
@dev_permission.require()
def dev_chart(days=7):
    dayrange=[]
    today = date.today()
    dayrange.append(str(today))
    for day in range(1,days):
        datetmp = today-timedelta(days=day)
        dayrange.append(str(datetmp))
    dayrange.sort()

    daycounts=[]
    for i in range(len(dayrange)):
        daycount=Work.query.filter(Work.dev == current_user.name, Work.create_time.like(dayrange[i]+'%')).count()
        daycounts.append(daycount)
    sevendayago = today-timedelta(days=days)
    works = Work.query.filter(Work.dev == current_user.name, Work.create_time >= sevendayago).group_by(Work.status)
    workstatus={u'正常结束':0, u'待人工审核':0, u'自动审核失败':0, u'执行中':0, u'执行异常':0, u'开发人中止':0, u'审核人中止':0, u'管理员中止':0, u'审核人驳回':0}
    for work in works:
        if work.status == 0:
            workstatus[u'正常结束']+=1
        elif work.status == 1:
            workstatus[u'待人工审核']+=1
        elif work.status == 2:
            workstatus[u'自动审核失败']+=1
        elif work.status == 3:
            workstatus[u'执行中']+=1
        elif work.status == 4:
            workstatus[u'执行异常']+=1
        elif work.status == 5:
            workstatus[u'开发人中止']+=1
        elif work.status == 6:
            workstatus[u'审核人中止']+=1
        elif work.status == 7:
            workstatus[u'管理员中止']+=1
        elif work.status == 8:
            workstatus[u'审核人驳回']+=1


    return render_template('dev_chart.html',dayrange=dayrange, daycounts=daycounts, workstatus=workstatus, days=days)








@app.route('/audit_work')
@audit_permission.require()
def audit_work():
    works = Work.query.filter(Work.audit == current_user.name, Work.status != 1)
    return render_template('audit_work.html', works=works)
@app.route('/audit_work_pending')
@audit_permission.require()
def audit_work_pending():
    works = Work.query.filter(Work.audit == current_user.name, Work.status == 1)
    return render_template('audit_work_pending.html', works=works)
@app.route('/audit_work/assign/<int:id>', methods = ['GET', 'POST'])
@audit_permission.require()
def audit_work_assign(id):
    work = Work.query.get(id)
    audits = User.query.filter(User.role == 'audit', User.srole == 0)
    form=WorkAssignForm()
    if form.validate_on_submit():
        work.srole = 0
        work.audit = form.audit.data
        db.session.commit()


        if mailonoff == 'ON':
            audit=User.query.filter(User.name == work.audit).first()
            send_email(u'【inception_web】分派工单通知', u'您好，你有一条分派的工单（' + work.name + u'），请审核，谢谢！', audit.email)
        return redirect('audit_work')

    return render_template('audit_work_assign.html', form=form, work=work, audits=audits)

@app.route('/audit_work/reject/<int:id>')
@audit_permission.require()
def audit_work_reject(id):
    work = Work.query.filter(Work.id == id).first()
    work.status = 8
    db.session.commit()
    stoptimer(work)
    flash(u'驳回工单成功！')
    return redirect('audit_work')

@app.route('/audit_work/execute/<int:id>')
@audit_permission.require()
def audit_work_execute(id):


    t=Thread(target=executeFinal,args=(id,))
    t.start()

    if mailonoff == 'ON':
        work = Work.query.filter(Work.id == id).first()
        dev = User.query.filter(User.name == work.dev).first()
        send_email(u'【inception_web】完成工单通知', u'您好，你发起的工单（' + work.name + u'）已执行，请稍后查看结果，谢谢！', dev.email)


    return redirect('audit_work')
@app.route('/audit_work/timer/<int:id>', methods = ['GET', 'POST'])
@audit_permission.require()
def audit_work_timer(id):
    work=Work.query.get(id)
    if request.method == "POST":
        data=request.form
        timer=datetime.strptime(data["dt"], "%Y-%m-%dT%H:%M")
        executetime = (timer - datetime.now()).seconds
        if executetime > 0 and work.status == 1:
            stoptimer(work)
            work.timer=timer
            db.session.commit()
            starttimer(work, executetime)
        else:
            flash(u'已过时间点')
    return render_template('audit_work_timer.html', work=work)
@app.route('/audit_work/timer/cancel/<int:id>')
@audit_permission.require()
def audit_work_timer_cancel(id):
    work = Work.query.get(id)
    stoptimer(work)
    work.timer = None
    db.session.commit()
    return redirect(url_for('audit_work_timer',id=id))
@app.route('/audit_work/timer/view')
@audit_permission.require()
def audit_work_timer_view():
    works=[]
    for item in threading.enumerate():
        if item.name:
            work=Work.query.filter(Work.name==item.name).first()
            if work:
                works.append(work)
    return render_template('audit_work_timer_view.html', works=works)




@app.route('/audit_work/exportsql/<int:id>')
#@audit_permission.require()
def audit_work_exportsql(id):
    #listSqlBak = inc.getRollbackSqlList(id)
    listSqlBak = getRollbackSqlList(id)
    base_dir = os.path.dirname(__file__)
    tmp_dir = base_dir+'/temp'
    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)
    fp = open(tmp_dir + '/backup.sql', 'w')
    for i in range(len(listSqlBak)):
        fp.write(listSqlBak[i]+'\n')
    fp.close()
    response = make_response(send_file(tmp_dir + '/backup.sql'))
    response.headers["Content-Disposition"] = "attachment; filename=ex.sql;"
    return response
@app.route('/audit_chart/<int:days>')
@audit_permission.require()
def audit_chart(days=7):
    dayrange=[]
    today = date.today()
    dayrange.append(str(today))
    for day in range(1,days):
        datetmp = today-timedelta(days=day)
        dayrange.append(str(datetmp))
    dayrange.sort()

    daycounts=[]
    for i in range(len(dayrange)):
        daycount=Work.query.filter(Work.audit == current_user.name, Work.create_time.like(dayrange[i]+'%')).count()
        daycounts.append(daycount)
    sevendayago = today-timedelta(days=days)

    works = db.session.query(Work.status).filter(Work.audit == current_user.name, Work.create_time >= sevendayago)

    workstatus={u'正常结束':0, u'待人工审核':0, u'自动审核失败':0, u'执行中':0, u'执行异常':0, u'开发人中止':0, u'审核人中止':0, u'管理员中止':0, u'审核人驳回':0}
    for work in works:
        if work.status == 0:
            workstatus[u'正常结束']+=1
        elif work.status == 1:
            workstatus[u'待人工审核']+=1
        elif work.status == 2:
            workstatus[u'自动审核失败']+=1
        elif work.status == 3:
            workstatus[u'执行中'] += 1
        elif work.status == 4:
            workstatus[u'执行异常']+=1
        elif work.status == 5:
            workstatus[u'开发人中止']+=1
        elif work.status == 6:
            workstatus[u'审核人中止']+=1
        elif work.status == 7:
            workstatus[u'管理员中止']+=1
        elif work.status == 8:
            workstatus[u'审核人驳回']+=1




    return render_template('audit_chart.html',dayrange=dayrange, daycounts=daycounts, workstatus=workstatus, days=days)





@app.route('/work/view/<int:id>')
@login_required
def work_view(id):
    work = Work.query.get(id)
    backtimer=0
    for item in threading.enumerate():
        if item.name == work.name:
            backtimer=1
    if work.status == 0:
        review_content=json.loads(work.execute_result)
    else:
        review_content=json.loads(work.auto_review)
    return render_template('work_view.html', work=work, review_content=review_content,backtimer=backtimer)

@app.route('/work/stop/<int:id>')
@login_required
def work_stop(id):
    work = Work.query.get(id)
    stoptimer(work)


    if current_user.role == 'dev':
        work.status = 5
        work.finish_time = datetime.now()
        db.session.commit()
        if mailonoff == 'ON':
            stop_email(work)
        return redirect('dev_work')
    elif current_user.role == 'audit':
        work.status = 6
        work.finish_time = datetime.now()
        db.session.commit()
        if mailonoff == 'ON':
            stop_email(work)
        return redirect('audit_work')
    elif current_user.role == 'admin':
        work.status = 7
        work.finish_time = datetime.now()
        db.session.commit()
        if mailonoff == 'ON':
            stop_email(work)
def stop_email(work):
    dev = User.query.filter(User.name == work.dev).first()
    audit = User.query.filter(User.name == work.audit).first()
    send_email(u'【inception_web】中止工单通知', u'您好，你有一条工单（' + work.name + u'）已被'+current_user.name+u'中止，请知悉，谢谢！', dev.email)
    send_email(u'【inception_web】中止工单通知', u'您好，你有一条工单（' + work.name + u'）已被'+current_user.name+u'中止，请知悉，谢谢！', audit.email)








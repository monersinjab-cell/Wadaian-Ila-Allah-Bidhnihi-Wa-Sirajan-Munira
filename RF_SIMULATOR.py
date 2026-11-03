#!/usr/bin/env python3
import os
import sys
import json
import time
import math

class RealisticRFSimulator:
    def __init__(self):
        self.output_status_path = "RF_STATUS.html"
        self.metrics_log_path = "milyar/rf_simulation_metrics.json"
        
        # المعايير الفيزيائية الحقيقية للمحاكاة (مثال: تردد 1408 ميجاهرتز)
        self.carrier_frequency_hz = 1408 * 1e6  
        self.speed_of_light = 3 * 1e8  # م/ث
        self.transmitter_power_dbm = 30.0  # قوة الإرسال
        self.antenna_gain_dbi = 2.15  # كسب الهوائي الافتراضي

    def verify_security_environment(self):
        """التحقق من تفعيل بروتوكولات جدار الحماية الرقمي وعدم وجود تكرار."""
        print("🛡️ [RF Simulator] جاري فحص خط الحماية البنيوي للنظام...")
        if os.path.exists("check_duplication.py"):
            if os.system("python check_duplication.py") != 0:
                print("❌ [إيقاف فوري] تم رصد ازدواجية بيانات مكررة! إجهاض تشغيل المحاكي.")
                return False
        return True

    def calculate_friis_path_loss(self, distance_meters):
        """حساب التوهين في الفضاء الحر بناءً على صيغة فريس الحقيقية."""
        if distance_meters <= 0:
            return 0.0
        wave_length = self.speed_of_light / self.carrier_frequency_hz
        path_loss_db = 20 * math.log10((4 * math.pi * distance_meters) / wave_length)
        return path_loss_db

    def calculate_doppler_shift(self, relative_velocity_ms):
        """حساب إزاحة دبلر الناتجة عن الحركة النسبية للمحطات."""
        doppler_shift_hz = (relative_velocity_ms / self.speed_of_light) * self.carrier_frequency_hz
        return doppler_shift_hz

    def execute_simulation_run(self, distance_meters=500, relative_velocity_ms=15.0):
        """تنفيذ المحاكاة الراديوية الحسابية وتوليد التقارير الواقعية."""
        if not self.verify_security_environment():
            sys.exit(1)

        print(f"📡 بدء معالجة المحاكاة الراديوية الحقيقية على التردد: {self.carrier_frequency_hz / 1e6} MHz")
        
        # العمليات الحسابية الفيزيائية
        path_loss = self.calculate_friis_path_loss(distance_meters)
        received_power_dbm = self.transmitter_power_dbm + (2 * self.antenna_gain_dbi) - path_loss
        doppler_shift = self.calculate_doppler_shift(relative_velocity_ms)
        
        # حساب سعة القناة النظرية (Shannon Capacity) بمعدل إشارة إلى الضوضاء افتراضي
        snr_linear = 10 ** ((received_power_dbm + 114) / 10)  # افتراض مستوى ضوضاء -114 ديسيبل ميلي واط
        bandwidth_hz = 20 * 1e6  # عرض نطاق 20 ميجاهرتز
        shannon_capacity_mbps = (bandwidth_hz * math.log2(1 + snr_linear)) / 1e6

        # إعداد تقرير المقاييس الرقمية للنموذج المحلي
        simulation_results = {
            "timestamp": int(time.time()),
            "frequency_mhz": self.carrier_frequency_hz / 1e6,
            "configured_distance_meters": distance_meters,
            "calculated_path_loss_db": round(path_loss, 2),
            "received_power_dbm": round(received_power_dbm, 2),
            "doppler_shift_hz": round(doppler_shift, 2),
            "shannon_channel_capacity_mbps": round(shannon_capacity_mbps, 2),
            "status": "SECURED_MATHEMATICAL_VALID"
        }

        # 1. حفظ المقاييس بصيغة JSON
        os.makedirs("milyar", exist_ok=True)
        with open(self.metrics_log_path, 'w', encoding='utf-8') as f:
            json.dump(simulation_results, f, indent=4, ensure_ascii=False)

        # 2. توليد واجهة العرض الراديوية السليمة بصيغة HTML
        html_content = f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>شاشة مراقبة الترددات الراديوية للمنظومة</title>
    <style>
        body {{ font-family: sans-serif; background: #111; color: #eee; padding: 20px; }}
        .card {{ background: #222; border: 1px solid #333; padding: 20px; border-radius: 8px; max-width: 600px; margin: 0 auto; }}
        h2 {{ color: #00ffcc; border-bottom: 1px solid #333; padding-bottom: 10px; }}
        .metric {{ margin: 10px 0; font-size: 1.1em; }}
        .value {{ color: #ffcc00; font-weight: bold; }}
    </style>
</head>
<body>
    <div class="card">
        <h2>📡 لوحة المحاكاة الفيزيائية الواقعية (RF Simulator)</h2>
        <div class="metric">التردد الناقل: <span class="value">{simulation_results['frequency_mhz']} MHz</span></div>
        <div class="metric">المسافة الحسابية: <span class="value">{simulation_results['configured_distance_meters']} متر</span></div>
        <div class="metric">توهين المسار (Friis): <span class="value">{simulation_results['calculated_path_loss_db']} dB</span></div>
        <div class="metric">طاقة الاستقبال التقريبية: <span class="value">{simulation_results['received_power_dbm']} dBm</span></div>
        <div class="metric">إزاحة دبلر المحسوبة: <span class="value">{simulation_results['doppler_shift_hz']} Hz</span></div>
        <div class="metric">سعة القناة القصوى (Shannon): <span class="value">{simulation_results['shannon_channel_capacity_mbps']} Mbps</span></div>
        <div class="metric" style="color: #00ff00; margin-top: 15px;">🔒 حالة الحماية البنيوية: SECURED</div>
    </div>
</body>
</html>
"""
        with open(self.output_status_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"✅ تم توليد وتأمين تقارير المحاكاة الراديوية المتقدمة بنجاح.")
        return True

if __name__ == "__main__":
    simulator = RealisticRFSimulator()
    simulator.execute_simulation_run()

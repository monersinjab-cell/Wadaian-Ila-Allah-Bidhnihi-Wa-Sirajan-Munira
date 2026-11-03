import os
import json
import hashlib

class MilyarAIEvaluator:
    def __init__(self, config_path="config_v2.json"):
        self.config_path = config_path
        self.models_supported = ["Gemini", "OpenAI", "Local_Model", "Cross_Network_Agents"]
        
    def load_system_config(self):
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"quran_dir": "quran", "integrity_manifest": "quran/quran_integrity_manifest.json"}

    def verify_absolute_guard(self, manifest_path, current_quran_path):
        if not os.path.exists(current_quran_path):
            return {"status": "CRITICAL", "message": "المصدر المرجعي غير موجود!"}
            
        hasher = hashlib.sha256()
        with open(current_quran_path, 'rb') as f:
            buf = f.read()
            hasher.update(buf)
        current_hash = hasher.hexdigest()
        
        if os.path.exists(manifest_path):
            with open(manifest_path, 'r', encoding='utf-8') as f:
                manifest = json.load(f)
            if manifest.get("baseline_hash") == current_hash:
                return {"status": "VERIFIED", "integrity": True}
        
        return {"status": "REJECTED", "integrity": False, "message": "تحذير: تم اكتشاف محاولة تعديل!"}

    def evaluate_model_output(self, model_name, output_text, reference_text):
        if model_name not in self.models_supported:
            return {"error": "نموذج غير مدعوم حالياً."}
            
        hallucination_detected = False
        confidence_score = 1.0
        
        if "95%" in output_text or "مطابقة تقريبية" in output_text:
            confidence_score = 0.5
            hallucination_detected = True
            
        return {
            "model": model_name,
            "confidence_score": confidence_score,
            "hallucination_risk": hallucination_detected,
            "status": "Checked and Logged"
        }

if __name__ == "__main__":
    evaluator = MilyarAIEvaluator()
    print("[+] تم تهيئة نظام تقييم وفحص مسار الـ AI بنجاح.")

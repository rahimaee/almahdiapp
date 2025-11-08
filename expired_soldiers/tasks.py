from threading import Thread
from .models import ExpiredSoldier
import uuid
from django.forms.models import model_to_dict

class ProcessingManager:
    active_tasks = {}  # key = filename, value = dict status

    @staticmethod
    def clean_finished_tasks():
        """
        حذف تسک‌های تمام‌شده بعد از چند ثانیه
        """
        finished = [key for key, val in ProcessingManager.active_tasks.items() if val.get('finished')]
        for f in finished:
            del ProcessingManager.active_tasks[f]

    @staticmethod
    def get_task(filename):
        if filename in ProcessingManager.active_tasks:
            return ProcessingManager.active_tasks[filename]
        return None
    
    @staticmethod
    def is_processing(filename):
        return filename in ProcessingManager.active_tasks


    @staticmethod
    def get_task_id(filename):
        if filename in ProcessingManager.active_tasks:
            task = ProcessingManager.active_tasks[filename]
            return task['task_id']
    
        return None
    @staticmethod
    def get_task_finished(filename):
        if filename in ProcessingManager.active_tasks:
            return ProcessingManager.active_tasks[filename]['finished'] == True
    
        return True
    
    @staticmethod
    def list_processing_tasks():
        return list(ProcessingManager.active_tasks.values())

    @staticmethod
    def list_processing_files():
        return list(ProcessingManager.active_tasks.keys())
    
    @staticmethod
    def start_processing(filename, records):
        """
        شروع پردازش فایل در Thread جداگانه
        """
        def task():
            total_count = len(records)
            processed_count = 0
            error_count = 0
            last_processed = []

            # اضافه کردن به active_tasks
            ProcessingManager.active_tasks[filename] = {
                'task_id':str(uuid.uuid4()), 
                'filename':filename,
                "total_count": total_count,
                "processed_count": processed_count,
                "error_count": error_count,
                "last_processed": last_processed,
                'finished':False,
            }

            for record in records:
                try:
                    saved, message, data, is_updated = ExpiredSoldier.save_record(record)
                    data_dict = data
                    if saved:
                        processed_count += 1
                        data_dict = model_to_dict(data)
                    else:
                        error_count += 1
                    
                    data_dict.update({
                        "__saved": saved,
                        "__message": message,
                        "__updated": is_updated
                    })
                    last_processed.append(data_dict)
                    last_processed = last_processed[-50:]

                except Exception:
                    error_count += 1


                # بروزرسانی وضعیت
                ProcessingManager.active_tasks[filename].update({
                    "processed_count": processed_count,
                    "error_count": error_count,
                    "last_processed": last_processed
                })

            # پایان پردازش
            ProcessingManager.active_tasks[filename]['finished'] = True
                           # حذف خودکار بعد از چند ثانیه
        
        t = Thread(target=task, daemon=True)
        t.start()
        return True

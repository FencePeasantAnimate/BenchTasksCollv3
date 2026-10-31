import os
import subprocess
import sys

TASKS = ['activity-logger', 'alert-system', 'analytics-dashboard', 'asset-optimizer', 'backup-utility', 'blog-engine', 'booking-system', 'cache-optimizer', 'calendar-sync', 'canvas-automation', 'canvas-grade-automation', 'certificate-manager', 'chat-bot', 'cms-builder', 'contact-manager', 'content-manager', 'content-scheduler', 'coupon-manager', 'crm-system', 'customer-feedback-processor', 'data-analytics', 'data-validator', 'deal-manager', 'deployment-tool', 'discount-calculator', 'email-campaign', 'email-classification-system', 'error-tracker', 'expense-tracker', 'feedback-collector', 'file-manager', 'follow-up-reminder', 'form-builder', 'health-monitor', 'help-desk', 'image-processor', 'inventory-management', 'invoice-generator', 'load-balancer', 'log-analyzer', 'loyalty-program', 'media-organizer', 'monitoring-agent', 'network-analyzer', 'order-processor', 'payment-processor', 'pdf-report-generator', 'permission-manager', 'personalization-service', 'price-tracker', 'product-catalog', 'qr-generator', 'reminder-service', 'robots-handler', 'sales-pipeline', 'scheduler', 'search-engine', 'security-scanner', 'sentiment-analyzer', 'shipment-tracker', 'social-connector', 'social-publisher', 'status-checker', 'storage-manager', 'streaming-service', 'subtitle-generator', 'survey-builder', 'sync-service', 'tag-manager', 'task-scheduler', 'template-engine', 'territory-manager', 'translation-api', 'video-trimmer', 'voice-processor', 'web-crawler']
BRANCHES = ['fan-dev', 'gyy', 'haoze', 'jl_dev', 'junteng_dev', 'junxian_dev', 'lueyang-dev', 'lv', 'ruige', 'wenshuo-dev', 'xiaochen_dev', 'yuxuan-dev', 'yuzhen-dev', 'zhaochen']

def git(*args):
    return subprocess.check_output(["git"] + list(args), text=True)

def main():
    os.makedirs("tasks/finalpool", exist_ok=True)
    copied = []
    for task in TASKS:
        found = False
        for branch in BRANCHES:
            try:
                files = git("ls-tree", "-r", "--name-only", f"origin/{branch}", "tasks").splitlines()
            except subprocess.CalledProcessError:
                continue
            prefix = None
            for f in files:
                if f.startswith("tasks/") and f.split("/")[-2] == task:
                    prefix = "/".join(f.split("/")[:-1])
                    break
            if not prefix:
                continue
            for f in files:
                if f.startswith(prefix + "/"):
                    content = subprocess.check_output(["git", "show", f"origin/{branch}:{f}"])
                    rel = f[len(prefix)+1:]
                    dest = os.path.join("tasks/finalpool", task, rel)
                    os.makedirs(os.path.dirname(dest), exist_ok=True)
                    with open(dest, "wb") as fh:
                        fh.write(content)
            found = True
            copied.append((task, branch, prefix))
            break
        if not found:
            print(f"WARNING: task not found: {task}", file=sys.stderr)
    with open("tasks/finalpool/readme.txt", "w", encoding="utf-8") as fh:
        fh.write("Final pool of implemented tasks from BenchTasksCollv3.\n")
    print(f"Copied {len(copied)} tasks")
    for item in copied:
        print(item)

if __name__ == "__main__":
    main()

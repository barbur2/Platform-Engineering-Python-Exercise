# Platform-Engineering-Python-Exercise
📌 מה הכלי עושה
כלי CLI ב־Python לניהול משאבי AWS (EC2, S3, Route53) עבור צוותי פיתוח, עם כללים מוגדרים מראש וסטנדרטים אחידים.
הכלי נועד להקל על מפתחים לבקש משאבים בעצמם, תוך שמירה על בקרה, אבטחה ותקינה ארגונית.
⚙️ דרישות מקדימות
Python 3.9+
חשבון AWS עם הרשאות מתאימות (EC2, S3, Route53).
פרופיל AWS מוגדר (aws configure).
חבילת boto3 מותקנת.
🛠 התקנה
git clone <repo-url>
cd platform-cli
pip install -r requirements.txt
🚀 שימוש בסיסי
הפורמט הכללי:
python cli.py <resource> <action> [options]
דוגמאות EC2
# יצירת אינסטנס מסוג t3.micro עם תגיות
python cli.py ec2 create --type t3.micro --owner bar --project demo

# רשימת אינסטנסים שנוצרו ע"י ה־CLI
python cli.py ec2 list

# עצירה/הפעלה של אינסטנס לפי ID
python cli.py ec2 stop --id i-1234567890abcdef
python cli.py ec2 start --id i-1234567890abcdef
דוגמאות S3
# יצירת bucket פרטי
python cli.py s3 create --name my-private-bucket --private

# יצירת bucket ציבורי (דורש אישור yes/no)
python cli.py s3 create --name my-public-bucket --public

# העלאת קובץ ל־bucket
python cli.py s3 upload --bucket my-private-bucket --file test.txt

# רשימת כל ה־buckets שנוצרו ע"י CLI
python cli.py s3 list
דוגמאות Route53
# יצירת Hosted Zone
python cli.py route53 create-zone --name example.com

# יצירת רשומת A
python cli.py route53 create-record --zone example.com --type A --name www --value 1.2.3.4

# רשימת רשומות
python cli.py route53 list --zone example.com
🏷 קונבנציית Tagging
כל משאב שנוצר ע"י הכלי מתויג באופן אחיד:
CreatedBy=platform-cli
Owner=<username>
Project=<project>
Environment=<env>
🧹 ניקוי משאבים (Cleanup)
כדי למחוק את כל המשאבים שנוצרו ע"י CLI:
python cli.py cleanup
הפקודה מוחקת EC2, S3, ו־Route53 עם התג CreatedBy=platform-cli.
🔐 אבטחה
הכלי לא שומר סודות בקוד.
חיבור מתבצע דרך AWS Profile / IAM Roles בלבד.
ברירת מחדל: S3 Buckets פרטיים, אחסון מוצפן.
📸 דמו Evidence
(להוסיף צילומי מסך / קטעי פקודות שהרצת)
EC2: יצירה + list + start/stop.
S3: יצירה + העלאת קובץ + list.
Route53: יצירת Zone + רשומת DNS.
🎁 בונוס (אופציונלי – אם מימשת)
UI (Flask / Streamlit / Tkinter) → מאפשר ניהול דרך טפסים/דשבורד.
בדיקות אוטומטיות עם pytest.

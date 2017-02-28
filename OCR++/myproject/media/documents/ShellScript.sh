directory="/var/www/html/OCR++/myproject/media/documents/"
source ~/virtual_env/v1/bin/activate
python $directory/main_script_batch.py
cp $directory/eval_* /var/www/html/media/documents/
cp $directory/*.xml /var/www/html/media/documents/


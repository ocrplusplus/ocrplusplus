# OCR++ : A Framework to extract information from Scholarly Articles 

NOTE : The tool works only on Linux-based systems

##### Installation : 
  - Install the dependencies.
  - Clone this repo and copy the OCR++ folder in  **/var/www/html** and make a directory named "**media**" in **/var/www/html**
  
      ```sh
      git clone https://github.com/ocrplusplus/ocrplusplus
      cd ocrplusplus
      mkdir -p /var/www/html/media
      mkdir -p /var/www/html/media/documents
      cp -r OCR++ /var/www/html/ 
      ```

##### Usage:
  - ###### With localhost as server :
    - Run the following commands : 
    
        ```sh
        cd /var/www/html/OCR++
        python manage.py runserver
        ```
    - Now open a web-browser and go to **127.0.0.1:8000/home**
    
  - ###### Without a server : 
    - Rename and cpoy the pdf as "**input.pdf**" on which you want to run OCR++ in the given directory using the command 
    
        ```sh
        cp path/to/pdf /var/www/html/OCR++/myproject/media/documents/input.pdf
        ```
    - run the OCR++ engine by running the Script
    
        ```sh
        cd /var/www/html/OCR++/myproject/media/documents/
        python main_script_batch.py
        ```

##### Dependencies:
    - nltk (maxent_pos_tagger + averaged_perceptron_tagger)
    - django <=v1.8
    - crfpp (Try downloading the source from http://www.filewatcher.com/m/CRF++-0.58.tar.gz.790570-0.html)
    

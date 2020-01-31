import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.io.InputStreamReader;

public class PacketExtr {
    public static void main(String[] args) throws Exception {
        File f=  new File(args[0]);
        File output = new File(args[1]);
        FileOutputStream fos = new FileOutputStream(output);
        FileInputStream is = new FileInputStream(f);
        BufferedInputStream reader = null;
		BufferedOutputStream writer = null;
        reader = new BufferedInputStream(is);
		writer = new BufferedOutputStream(fos);

        int byteRead;
        int count =6; //my "size: "
        int tobeRead = 0;
        byte[] buff = new byte[4096];

        while ((byteRead = reader.read(buff)) != -1) {
            if(tobeRead!=0){ //output
               while(tobeRead!=0){ //output
                writer.write(buff, 0, byteRead);
                tobeRead--; //decremenet number of byte to be read
               }
            }
            if(count==0){ //size : is passed, get number now
                char readChar = (char)byteRead;
                String num = "";
                while(readChar!='B'){
                    num = num + readChar;
                    readChar = (char)byteRead;
                }

                tobeRead = Integer.parseInt(num);
                count = 6;
            }
            count--;
            
        }

    }
}
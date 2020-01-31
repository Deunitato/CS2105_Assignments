import java.io.ByteArrayOutputStream;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.zip.CRC32;

public class Checksum{

//note: Tutorial taken in reference to: http://scalebean.blogspot.com/2015/02/crc32-calculation-on-java-and-objective.html
  public static void main(String args[]){
    try{
        Path path = Paths.get("test/test.jpg");
        byte[] data = Files.readAllBytes(path);

        CRC32 checksum = new CRC32();
        checksum.update(data, 0, data.length);
        System.out.println(checksum.getValue());
    }
    catch(IOException e){
        e.printStackTrace();
    }
   }
}
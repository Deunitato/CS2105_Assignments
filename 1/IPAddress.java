import java.util.Scanner;

public class IPAddress {

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        String bits = sc.nextLine();
        int[] IParr = getIP(bits);
        //print it

        for(int bin : IParr){
            System.out.print(bin+".");
        }
    }

    public static int[] getIP(String bit){

        int[] newArr = new int[4];
        //split
        for(int i = 0 ; i < 4 ; i ++){
            int start = i*8;
            String s = bit.substring(start, start+8);
            newArr[i] = binStringtoInt(s);
        }

        return newArr;
        //convert each string to boolean

    }


    public static int binStringtoInt(String s){
        double sum =0;
        int power = 0;
        for(int i = 7 ; i >=0 ; i --){
            char character = s.charAt(i);
            if(character=='1'){
                sum = sum + Math.pow(2,power);
            }
            power++;
        }

        return (int)sum;
    }
}
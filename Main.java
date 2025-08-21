public class Main {
    public static void main(String[] args) {
        if (args.length < 2) {
            System.out.println("Please provide two numbers as parameters.");
            return;
        }
        try {
            int num1 = Integer.parseInt(args[0]);
            int num2 = Integer.parseInt(args[1]);

            System.out.println("First number: " + num1);
            System.out.println("Second number: " + num2);
            System.out.println("Sum = " + (num1 + num2));
            System.out.println("Difference = " + (num1 - num2));
            System.out.println("Product = " + (num1 * num2));

            if (num2 != 0) {
                System.out.println("Quotient = " + (num1 / num2));
                System.out.println("Remainder = " + (num1 % num2));
            } else {
                System.out.println("Division by zero not allowed.");
            }
        } catch (NumberFormatException e) {
            System.out.println("Invalid input. Please enter integers.");
        }
    }
}




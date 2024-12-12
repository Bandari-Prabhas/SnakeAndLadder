public class Dice {
     private int numberOfDice;

     public Dice(int numberOfDice) {
          this.numberOfDice = numberOfDice;
     }

     public int getNumberOfDice() {
          return numberOfDice;
     }

     public void setNumberOfDice(int numberOfDice) {
          this.numberOfDice = numberOfDice;
     }

     public int rollDice() {
          return (int) (Math.random() * 6 * numberOfDice) + 1;
     }
}
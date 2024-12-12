import java.util.*;

public class GameBoard {
     private Dice dice;
     private Queue<Player> nextTurn;
     private List<Jumper> snakes;
     private List<Jumper> ladders;
     private Map<String, Integer> playersCurrentPosition;
     private int boardSize;

     public GameBoard(Dice dice, Queue<Player> nextTurn, List<Jumper> snakes, List<Jumper> ladders,
               Map<String, Integer> playersCurrentPosition, int boardSize) {
          this.dice = dice;
          this.nextTurn = nextTurn;
          this.snakes = snakes;
          this.ladders = ladders;
          this.playersCurrentPosition = playersCurrentPosition;
          this.boardSize = boardSize;
     }

     public void startGame() {
          while (nextTurn.size() > 1) {
               Player player = nextTurn.poll();
               int currentPosition = playersCurrentPosition.get(player.getName());
               int diceValue = dice.rollDice();
               int nextCell = currentPosition + diceValue;

               if (nextCell > boardSize) {

                    nextTurn.offer(player);
               } else if (nextCell == boardSize) {

                    System.out.println(player.getName() + " won the game");
               } else {
                    int finalPosition = nextCell;
                    boolean gotLadder = false;

                    for (Jumper snake : snakes) {
                         if (snake.getStart() == nextCell) {
                              finalPosition = snake.getEnd();
                              System.out.println(player.getName() + " was bitten by a snake at: " + nextCell);
                              break;
                         }
                    }

                    for (Jumper ladder : ladders) {
                         if (ladder.getStart() == nextCell) {
                              finalPosition = ladder.getEnd();
                              System.out.println(player.getName() + " climbed a ladder at: " + nextCell);
                              gotLadder = true;
                              break;
                         }
                    }

                    if (finalPosition == boardSize) {

                         System.out.println(player.getName() + " won the game");
                    } else {
                         playersCurrentPosition.put(player.getName(), finalPosition);
                         System.out.println(player.getName() + " is now at position " + finalPosition);
                         nextTurn.offer(player);
                    }
               }
          }
     }
}

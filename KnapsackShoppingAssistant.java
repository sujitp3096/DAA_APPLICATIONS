import java.util.*;

public class KnapsackShoppingAssistant {

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        // Input number of items
        System.out.print("Enter number of items: ");
        int n = sc.nextInt();

        int[] weight = new int[n];
        int[] value = new int[n];

        // Input weight and value of each item
        System.out.println("Enter weight and value of each item:");
        for (int i = 0; i < n; i++) {
            System.out.print("Item " + (i + 1) + " Weight: ");
            weight[i] = sc.nextInt();
            System.out.print("Item " + (i + 1) + " Value: ");
            value[i] = sc.nextInt();
        }

        // Knapsack capacity
        System.out.print("Enter maximum weight capacity: ");
        int capacity = sc.nextInt();

        // DP table
        int[][] dp = new int[n + 1][capacity + 1];

        // 0/1 Knapsack Algorithm
        for (int i = 1; i <= n; i++) {
            for (int w = 1; w <= capacity; w++) {
                if (weight[i - 1] <= w) {
                    dp[i][w] = Math.max(
                            value[i - 1] + dp[i - 1][w - weight[i - 1]],
                            dp[i - 1][w]
                    );
                } else {
                    dp[i][w] = dp[i - 1][w];
                }
            }
        }

        // Final result
        System.out.println("\nMaximum Value You Can Carry: " + dp[n][capacity]);

        // Trace selected items
        System.out.println("\nSelected Items:");
        int w = capacity;
        for (int i = n; i > 0; i--) {
            if (dp[i][w] != dp[i - 1][w]) {
                System.out.println(" → Item " + i + " (Weight: " + weight[i - 1] + ", Value: " + value[i - 1] + ")");
                w -= weight[i - 1];
            }
        }

        sc.close();
    }
}

import java.util.Scanner;

public class Acwing245 {
    public static void main(String[] args) {
        Scanner scan = new Scanner(System.in);
        int N = scan.nextInt();
        int M = scan.nextInt();
        SegmentTree stree = new SegmentTree(N, scan);
        stree.build(1, 1, N);
        scan.nextLine();
        for (int i = 0; i < M; i++) {
            String[] nums = scan.nextLine().split(" ");
            int x = Integer.valueOf(nums[1]), y = Integer.valueOf(nums[2]);
            if(nums[0].equals("1")){
                int ans = stree.query(1, Math.min(x, y), Math.max(x, y));
                System.out.println(ans);
            }else{
                stree.change(1, x, y);
            }
        }
    }
}

class SegmentTree{
    private class Node{
        int l, r, sum, lmax, rmax, max;
        public Node(int l, int r, int sum, int lmax, int rmax, int max){
            this.l = l; this.r = r; this.sum = sum; this.lmax = lmax; this.rmax = rmax; this.max = max;
        }
        public Node(int l, int r){
            this(l, r, 0, 0, 0, 0);
        }
    }
    Node[] nodes;
    Scanner scan;
    public SegmentTree(int N, Scanner scan){
        this.nodes = new Node[4 * N];
        this.scan = scan;
    }

    public void build(int i, int l, int r){
        nodes[i] = new Node(l, r);
        if(l == r){
            int v = scan.nextInt();
            nodes[i].sum = nodes[i].lmax = nodes[i].rmax = nodes[i].max = v;
            return;   
        }
        int mid = (l + r) >> 1;
        build(i << 1, l, mid);
        build(i << 1 | 1, mid + 1, r);
        push(nodes[i], nodes[i << 1], nodes[i << 1 | 1]);
    }

    public void change(int i, int x, int y){
        if(nodes[i].l == nodes[i].r){
            nodes[i].sum = nodes[i].lmax = nodes[i].rmax = nodes[i].max = y;
            return;
        }
        int mid = (nodes[i].l + nodes[i].r) >> 1;
        if(mid < x){
            change(i << 1 | 1, x, y);
        }else{
            change(i << 1, x, y);
        }
        push(nodes[i], nodes[i << 1], nodes[i << 1 | 1]);
    }

    public int query(int i, int l, int r){
        return ask(i, l, r).max;
    }

    private Node ask(int i, int l, int r){
        if(l <= nodes[i].l && nodes[i].r <= r){
            return nodes[i];
        }
        int mid = (nodes[i].l + nodes[i].r) >> 1;
        if(mid < l){
            return ask(i << 1 | 1, l, r);
        }
        if(r <= mid){
            return ask(i << 1, l, r);
        }
        Node root = new Node(l, r);
        Node left = ask(i << 1, l, r);
        Node right = ask(i << 1 | 1, l, r);
        push(root, left, right);
        return root;
    }

    private void push(Node root, Node left, Node right){
        root.sum = left.sum + right.sum;
        root.lmax = Math.max(left.lmax, left.sum + right.lmax);
        root.rmax = Math.max(right.rmax, right.sum + left.rmax);
        root.max = Math.max(Math.max(left.max, right.max), left.rmax + right.lmax);
    }
}
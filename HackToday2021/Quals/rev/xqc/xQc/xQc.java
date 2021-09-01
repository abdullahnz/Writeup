// 
// Decompiled by Procyon v0.5.36
// 

package xQc;

import java.awt.BorderLayout;
import QcX.QcX;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import javax.swing.Icon;
import javax.swing.ImageIcon;
import java.awt.Component;
import java.awt.Dimension;
import java.awt.Color;
import java.awt.FlowLayout;
import java.awt.LayoutManager;
import java.awt.GridLayout;
import javax.swing.JButton;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JFrame;

public class xQc extends JFrame
{
    private String[] symbols;
    private JPanel slotPanel;
    private JLabel[] slot;
    private JButton spin;
    
    public byte[] hash(final byte[] array) {
        long n = -3750763034362895579L;
        final long n2 = 1099511628211L;
        for (int i = 0; i < array.length; ++i) {
            n = (n ^ (long)(array[i] & 0xFF)) * n2;
        }
        final byte[] array2 = new byte[8];
        for (int j = 7; j >= 0; --j) {
            array2[j] = (byte)(n & 0xFFL);
            n >>= 8;
        }
        return array2;
    }
    
    public xQc() {
        this.symbols = new String[] { "Pepega", "xqcL", "Book", "EZ", "Clap", "OMEGALUL", "FeelsGoodMan", "TriHard" };
        this.slotPanel = new JPanel(new GridLayout(1, 9));
        this.slot = new JLabel[7];
        this.spin = new JButton("Spin");
        final JPanel comp = new JPanel(new GridLayout(2, 1));
        final JPanel comp2 = new JPanel(new FlowLayout(1, 5, 2));
        this.spin.setBackground(Color.ORANGE);
        this.spin.setPreferredSize(new Dimension(800, 40));
        comp2.add(this.spin);
        comp.add(comp2, "North");
        this.slot[0] = new JLabel(new ImageIcon(this.getClass().getResource("/images/left.png")));
        this.slot[1] = new JLabel(new ImageIcon(this.getClass().getResource("/images/center.png")));
        this.slot[2] = new JLabel(new ImageIcon(this.getClass().getResource("/images/center.png")));
        this.slot[3] = new JLabel(new ImageIcon(this.getClass().getResource("/images/center.png")));
        this.slot[4] = new JLabel(new ImageIcon(this.getClass().getResource("/images/center.png")));
        this.slot[5] = new JLabel(new ImageIcon(this.getClass().getResource("/images/center.png")));
        this.slot[6] = new JLabel(new ImageIcon(this.getClass().getResource("/images/center.png")));
        for (int i = 0; i < 7; ++i) {
            this.slotPanel.add(this.slot[i]);
        }
        this.spin.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(final ActionEvent actionEvent) {
                String s = "";
                for (int i = 0; i < 7; ++i) {
                    final int n = (int)(Math.random() * 8.0);
                    s = invokedynamic(makeConcatWithConstants:(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;, s, xQc.this.symbols[n]);
                    xQc.this.slot[i].setIcon(new ImageIcon(this.getClass().getResource(invokedynamic(makeConcatWithConstants:(Ljava/lang/String;)Ljava/lang/String;, xQc.this.symbols[n]))));
                }
                xQc.this.spin.setText(new QcX(xQc.this.hash(s.getBytes())).validate());
            }
        });
        final JPanel comp3 = new JPanel(new BorderLayout());
        comp3.add(comp, "East");
        final JPanel comp4 = new JPanel(new GridLayout(2, 1));
        comp4.add(this.slotPanel);
        comp4.add(comp3);
        this.add(comp4);
    }
    
    public static void main(final String[] array) {
        final xQc xQc = new xQc();
        xQc.setTitle("xQc");
        xQc.setLocationRelativeTo(null);
        xQc.setSize(800, 250);
        xQc.setDefaultCloseOperation(3);
        xQc.setResizable(false);
        xQc.setVisible(true);
    }
}

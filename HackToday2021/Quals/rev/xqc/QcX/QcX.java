// 
// Decompiled by Procyon v0.5.36
// 

package QcX;

public class QcX
{
    private final byte[] S;
    private final byte[] T;
    private final int keylen;
    
    public QcX(final byte[] array) {
        this.S = new byte[256];
        this.T = new byte[256];
        if (array.length < 1 || array.length > 256) {
            throw new IllegalArgumentException("key must be between 1 and 256 bytes");
        }
        this.keylen = array.length;
        for (int i = 0; i < 256; ++i) {
            this.S[i] = (byte)i;
            this.T[i] = array[i % this.keylen];
        }
        int n = 0;
        for (int j = 0; j < 256; ++j) {
            n = (n + this.S[j] + this.T[j] & 0xFF);
            final byte b = this.S[n];
            this.S[n] = this.S[j];
            this.S[j] = b;
        }
    }
    
    public String validate() {
        final String[] array = { "S OMEGALUL BAD", "TriHard7 TriHard7 TriHard7", "mad cuz bad", "LLLLLLLLLLLLLLLLLLLLLLLLLLLLLL" };
        final int n = (int)(Math.random() * 4.0);
        final byte[] hexStringToByteArray = hexStringToByteArray("91AD6CC96F93D0B1C41426A98E5E5C8BA6A372045EC20D21D2097257229C69779C69F699E09E6A74A45B587E085516E7CDE8");
        final byte[] bytes = new byte[hexStringToByteArray.length];
        int n2 = 0;
        int n3 = 0;
        for (int i = 0; i < hexStringToByteArray.length; ++i) {
            n2 = (n2 + 1 & 0xFF);
            n3 = (n3 + this.S[n2] & 0xFF);
            final byte b = this.S[n3];
            this.S[n3] = this.S[n2];
            this.S[n2] = b;
            bytes[i] = (byte)(hexStringToByteArray[i] ^ this.S[this.S[n2] + this.S[n3] & 0xFF]);
        }
        final String s = new String(bytes);
        if (s.contains("hacktoday")) {
            return s;
        }
        return array[n];
    }
    
    public static byte[] hexStringToByteArray(final String s) {
        final int length = s.length();
        final byte[] array = new byte[length / 2];
        for (int i = 0; i < length; i += 2) {
            array[i / 2] = (byte)((Character.digit(s.charAt(i), 16) << 4) + Character.digit(s.charAt(i + 1), 16));
        }
        return array;
    }
}

import java.io.File;

/*
 * Usage:
 * - compile: javac PathDirNameBaseName.java
 * - execute: java PathDirNameBaseName
 */

public class PathDirNameBaseName {
    public static void main(String [] args) {

        String path = "/home/user/fichier.txt";
        File file = new File(path);

        String basename = file.getName();
        String dirname  = file.getParent();

        System.out.println("Path: " + path);
        System.out.println("BaseName: " + basename);
        System.out.println("DirName: " + dirname);
    }
}

using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;
using System.Linq;
using System.Threading;

public class CodeAnimation : MonoBehaviour
{
    public GameObject[] Body;
    List<string> lines;
    int counter = 0;

    // Start is called before the first frame update
    void Start()
    {
        lines = System.IO.File.ReadLines("C:/Users/veyss/PoseEstimation/pose_landmarks.txt").ToList();
    }

    // Update is called once per frame
    void Update()
    {
        // create string with coordinate for each frame
        string[] points = lines[counter].Split(',');

        // Boucle for each sphere
        for (int i = 0; i<33; i++)
        {
            float x = float.Parse(points[0 + i * 3]) / 100;
            float y = float.Parse(points[1 + i * 3]) / 100;
            float z = float.Parse(points[2 + i * 3]) / 100;
            Body[i].transform.localPosition = new Vector3(x, y, z);
        }

        // indices get +1 to get to the next frame
        counter += 1;
        // if the counter is at the last frame frame, it will restart
        if (counter == lines.Count) { counter = 0; }
        Thread.Sleep(30);
    }
}

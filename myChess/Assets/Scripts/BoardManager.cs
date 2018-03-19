using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class BoardManager : MonoBehaviour {

    public static BoardManager Instance { get; set; }
    private bool[,] movesAllowed { set; get; }

    private const float TILE_SIZE = 1.0f;

    private const float TILE_OFFSET = .5f;

    private int selectionX = -1;
    private int selectionY = -1;
    private int tempX, tempY;

    public List<GameObject> chessPiecePrefabs;
    private List<GameObject> activePiece;

    private Material previousMaterial;
    public Material selectedMaterial;

    //this is the 2D array that will hold the chesspieces
    public Piece[,] Pieces { set; get; }


    public Piece selectedPiece;

    private bool isWhiteTurn = true;
    public bool isWhite;


    public int[] EnPassant { set; get; }

    private Client client;


    //this rotates all pieces 90 degrees, but it only matters for knight
    private Quaternion orientation = Quaternion.Euler(0, 90, 0);

    private void Start()
    {
        Instance = this;
        client = FindObjectOfType<Client>();
        isWhiteTurn = client.isHost;



        PopulateChessBoard();
    }



    public void Update()
    {
        UpDateSelection();
        DrawChessBoard();

        /*  if (Input.GetMouseButtonDown(0))
          {
              if (selectionX >= 0 && selectionY >= 0)
              {

                  if (selectedPiece == null)
                  {
                      SelectPiece(selectionX, selectionY);

                  }
                  else
                  {
                      MovePiece(selectionX, selectionY);
                  }
              }

          }
          */
        PlayerMove();
    



        
        
        
    }
    public void PlayerMove()
    {
        if (Input.GetMouseButtonDown(0))
        {
            if (selectionX >= 0 && selectionY >= 0)
            {

                string msg = "CSEL|";




                if (selectedPiece == null)
                {
                    //SelectPiece(selectionX, selectionY);
                    msg += Pieces[selectionX,selectionY].GetType() + "|";
                    msg += selectionX + "|";
                    msg += selectionY;
                    if (client)
                        client.Send(msg);
                }
                else
                {
                    //MovePiece(selectionX, selectionY);
                    msg = "CMOV|";
                    msg += selectionX + "|";
                    msg += selectionY;
                    if (client)
                        client.Send(msg);



                }




            }

        }
    }

    public void SelectPiece(int x, int y)
    {
        if (Pieces[x, y] == null)
            return;
        if (Pieces[x, y].isWhite != isWhiteTurn)
            return;

        bool hasAtleastOneMove = false;
		movesAllowed = Pieces [x, y].PossibleMove ();
        for (int i = 0; i < 8; i++)
            for (int j = 0; j < 8; j++)
                if (movesAllowed[i, j])
                    hasAtleastOneMove = true;

        if (!hasAtleastOneMove)
            return;

        selectedPiece = Pieces[x, y];


        previousMaterial = selectedPiece.GetComponent<MeshRenderer>().material;
        selectedMaterial.mainTexture = previousMaterial.mainTexture;
        selectedPiece.GetComponent<MeshRenderer>().material = selectedMaterial;
		HighlightBoard.Instance.highlightPossibleMoves (movesAllowed);



    }
    public void MovePiece(int x, int y)
    {
		if (movesAllowed[x,y])
        {
			
			Piece c = Pieces [x, y];
		/*	if (c.GetType () == typeof(King)) {
				//end game
				return;
			}
*/
			if (c != null && c.isWhite != isWhiteTurn) {

                //If it is the king
                if (c.GetType() == typeof(King))
                {
                    // End the game
                    EndGame();
                }

				activePiece.Remove (c.gameObject);
				Destroy (c.gameObject);
			}

            if(x == EnPassant[0] && y == EnPassant[1])
            {
                if(isWhiteTurn)
                    c = Pieces[x, y - 1];
                  
                else
                    c = Pieces[x, y + 1];
                activePiece.Remove(c.gameObject);
                Destroy(c.gameObject);

            }
            EnPassant[0] = -1;
            EnPassant[1] = -1;
            if(selectedPiece.GetType() == typeof(Pawn))
            {
                if(y == 7)
                {
                    activePiece.Remove(selectedPiece.gameObject);
                    Destroy(selectedPiece.gameObject);
                    SpawnChessPieces(1,x,y);
                    selectedPiece = Pieces[x, y];
                }
                else if (y == 0)
                {
                    activePiece.Remove(selectedPiece.gameObject);
                    Destroy(selectedPiece.gameObject);
                    SpawnChessPieces(7, x, y);
                    selectedPiece = Pieces[x, y];

                }
                if (selectedPiece.CurrentY == 1 && y == 3)
                {
                    EnPassant[0] = x;
                    EnPassant[1] = y - 1;
                }else if(selectedPiece.CurrentY == 6 && y == 4)
                {
                    EnPassant[0] = x;
                    EnPassant[1] = y + 1;
                }
                    
            }
            
            

            Pieces[selectedPiece.CurrentX, selectedPiece.CurrentY] = null;
            selectedPiece.transform.position = GetTileCenter(x, y);
			selectedPiece.SetPosition (x, y);
            Pieces[x, y] = selectedPiece;

         
                
            
            
            isWhiteTurn = !isWhiteTurn;
            
            

        }

        selectedPiece.GetComponent<MeshRenderer>().material = previousMaterial;

		HighlightBoard.Instance.hideTheHighlights ();
        selectedPiece = null;

    }


    //takes mouse position, and truncates to determine which tile the mouse is touching
    //if mouse is not touching a tile, then it is set to negative value
    private void UpDateSelection()
    {
        if (!Camera.main)
            return;

        RaycastHit hit;
        if (Physics.Raycast(Camera.main.ScreenPointToRay(Input.mousePosition), out hit, 25.0f, LayerMask.GetMask("ChessPlane")))
        {
            selectionX = (int)hit.point.x;
            selectionY = (int)hit.point.z;
        }
        else
        {
            selectionX = -1;
            selectionY = -1;
        }
    }

    private void SpawnChessPieces(int index, int x, int y)
    {
        

        //(had to use these lines like this because knights were still facing the wrong way)
        if (index == 10)
            orientation = Quaternion.Euler(0, 270, 0);

        
        
        GameObject go = Instantiate(chessPiecePrefabs[index], GetTileCenter(x,y), orientation) as GameObject;
        go.transform.SetParent(transform);
        Pieces[x, y] = go.GetComponent<Piece>();
        Pieces[x, y].SetPosition(x, y);
        activePiece.Add(go);




    }


    //draws the chess board using vectors, and draws an X on the tile that the mouse is touching
    private void DrawChessBoard()
    {
        Vector3 widthLine = Vector3.right * 8;
        Vector3 heightLine = Vector3.forward * 8;

        for(int x = 0; x <= 8; x++)
        {
            Vector3 start = Vector3.forward * x;
            Debug.DrawLine(start, start + widthLine);

            for(int y = 0; y <= 8; y++)
            {
                start = Vector3.right * y;
                Debug.DrawLine(start, start + heightLine);

            }
        }

        //draw selection
        if(selectionX >= 0 && selectionY >= 0)
        {
            Debug.DrawLine(
                Vector3.forward * selectionY + Vector3.right * selectionX,
                Vector3.forward * (selectionY + 1) + Vector3.right * (selectionX + 1));

            Debug.DrawLine(
                Vector3.forward * (selectionY + 1) + Vector3.right * selectionX,
                Vector3.forward * selectionY + Vector3.right * (selectionX + 1));
        }
    }


    //this is a helper function to help with the positioning on the piece models onto the chessboard tiles so that they are dead center
    private Vector3 GetTileCenter(int x, int y)
    {
        Vector3 origin = Vector3.zero;
        origin.x += (TILE_SIZE * x) + TILE_OFFSET;
        origin.z += (TILE_SIZE * y) + TILE_OFFSET;
        return origin;
    }


    //populates the chessboard with all models
    private void PopulateChessBoard()
    {
        activePiece = new List<GameObject>();
        
        Pieces = new Piece[8, 8];
        EnPassant = new int[2] { -1, -1 };
        
        //white pieces
        //king
        SpawnChessPieces(0, 3, 0);

        //queen
        SpawnChessPieces(1, 4, 0);

        //rook
        SpawnChessPieces(2, 0, 0);
        SpawnChessPieces(2, 7, 0);

        //bishop
        SpawnChessPieces(3, 2, 0);
        SpawnChessPieces(3, 5, 0);

        //knight
        SpawnChessPieces(4, 1, 0);
        SpawnChessPieces(4, 6, 0);

        //pawns
        for(int i = 0; i < 8; i++)
            SpawnChessPieces(5, i, 1);

        //blackpieces
        //king
        SpawnChessPieces(6, 4, 7);

        //queen
        SpawnChessPieces(7, 3, 7);

        //rook
        SpawnChessPieces(8, 0, 7);
        SpawnChessPieces(8, 7, 7);

        //bishop
        SpawnChessPieces(9, 2, 7);
        SpawnChessPieces(9, 5, 7);

        //knight
        SpawnChessPieces(10, 1, 7);
        SpawnChessPieces(10, 6, 7);

        //pawns
        for (int i = 0; i < 8; i++)
            SpawnChessPieces(11, i, 6);

        /*
        //dummy pieces
        for (int i = 0; i < 8; i++)
            SpawnChessPieces(12, i, 4);
		*/
        



    }
    private void EndGame()
    {

        // Need to fix white team not going again after winning
        if (isWhiteTurn)
            Debug.Log("White team wins");
        else
            Debug.Log("Black team wins");

        foreach (GameObject go in activePiece)
            Destroy(go);

        isWhiteTurn = false;
        HighlightBoard.Instance.hideTheHighlights();
        PopulateChessBoard();
    }
}

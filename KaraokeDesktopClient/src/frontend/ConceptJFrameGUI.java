package frontend;

import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Desktop;
import java.awt.Dimension;
import java.awt.GridLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;
import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.net.URI;
import java.net.URISyntaxException;
import java.net.URLEncoder;
import java.util.Arrays;

import javax.imageio.ImageIO;
import javax.swing.AbstractAction;
import javax.swing.AbstractButton;
import javax.swing.Action;
import javax.swing.BorderFactory;
import javax.swing.ImageIcon;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JMenu;
import javax.swing.JMenuBar;
import javax.swing.JMenuItem;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTable;
import javax.swing.JTextField;
import javax.swing.RowFilter;
import javax.swing.SwingConstants;
import javax.swing.UIManager;
import javax.swing.UnsupportedLookAndFeelException;
import javax.swing.event.DocumentEvent;
import javax.swing.event.DocumentListener;
import javax.swing.table.DefaultTableCellRenderer;
import javax.swing.table.DefaultTableModel;
import javax.swing.table.TableColumnModel;
import javax.swing.table.TableModel;
import javax.swing.table.TableRowSorter;

import backend.ActionHandler;

/**
 * The graphical user interface of this program. It combines the already written
 * back end code with a user friendly and feature rich graphical java swing
 * interface.
 * 
 * @author Niklas | https://github.com/AnonymerNiklasistanonym
 * @version 0.3 (beta)
 *
 */
public class ConceptJFrameGUI {

	/**
	 * All the management of the list and data already written
	 */
	private ActionHandler actionManager;

	/**
	 * global window where the main things will happen
	 */
	private JFrame guiMainFrame;

	// a global JTable and DefaultTableModel;
	private JTable table;
	private DefaultTableModel model;
	TableRowSorter<TableModel> rowSorter;

	/**
	 * Constructor: When an object of ConceptJFrameGUI gets produced this
	 * automatically will happen:
	 */
	public ConceptJFrameGUI() {

		String[] columnNames = new String[] { "#", "Artist", "Title" };
		String[] fileNameConfiguration = new String[] { "karaokeConfig", "cfg" };

		// start a new window/JFrame
		guiMainFrame = new JFrame();
		// start a ActionHandler for all the under the surface commands
		actionManager = new ActionHandler(columnNames, fileNameConfiguration);
	}

	/**
	 * At startup this method checks if a configuration file exist and loads it
	 * if it finds one. So a fast start for already set up party's/etc. is
	 * possible.
	 */
	public void startupConfig() {

		// if a configuration file exists
		if (actionManager.fileExists(actionManager.getConfigurationFile())) {
			// ask the user if he also wants to load saved data
			if (JOptionPane.showConfirmDialog(null, "Would you like to load your previous saved configuration? ",
					"Question", JOptionPane.YES_NO_OPTION, JOptionPane.QUESTION_MESSAGE) == JOptionPane.YES_OPTION) {
				// if he accepts to load the data read the file and set the
				// content as your new path list
				actionManager.configFileReader();
				// now scan again all paths for music videos
				actionManager.updateMusicVideoList();
			}
		}
	}

	/**
	 * This method manages the main graphic user interface. Here you can find
	 * all features.
	 * 
	 * @throws IOException
	 */
	public void createWindow() throws IOException {

		guiMainFrame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		// make sure the program exits when the frame closes
		guiMainFrame.setTitle("Karaoke Desktop Client [Beta]");
		// title of the window
		guiMainFrame.setSize(500, 620);
		// size of the window at the start
		guiMainFrame.setLocationRelativeTo(null);
		// let it pop up in the middle of the screen

		try {
			guiMainFrame.setIconImage(ImageIO.read(ConceptJFrameGUI.class.getResource("/logo.png")));
		} catch (IOException exc) {
			exc.printStackTrace();
		}

		// add a menu bar to the window
		JMenuBar menuBar = new JMenuBar();

		// with the sub menu "Source folders"
		JMenu subMenuPath = new JMenu("Source folders");
		subMenuPath.setToolTipText("Add/Change/Remove the actual folders of your music videos");
		// and the sub sub menu "Add" >>
		ImageIcon iconAdd = new ImageIcon(ImageIO.read(ConceptJFrameGUI.class.getResource("/add_20x20.png")));
		JMenuItem subSubMenuAddSourceFolder = new JMenuItem("Add", iconAdd);
		subSubMenuAddSourceFolder.setToolTipText("Add a new folder with new music videos to your list");
		subSubMenuAddSourceFolder.addActionListener((ActionEvent event) -> {
			System.out.println("Add a new folder with new music videos to your list");
			actionManager.addToPathList(actionManager.getPathOfDirectories());
			updateTable();
		});

		// and the sub sub menu "Remove" >>
		ImageIcon iconRemove = new ImageIcon(ImageIO.read(ConceptJFrameGUI.class.getResource("/remove_20x20.png")));
		JMenuItem subSubMenuRemoveSourceFolder = new JMenuItem("Remove", iconRemove);
		subSubMenuRemoveSourceFolder.setToolTipText("Remove a folder with music videos from your list");
		subSubMenuRemoveSourceFolder.addActionListener((ActionEvent event) -> {
			System.out.println("Remove a folder from your path list");
			if (actionManager.getPathList().isEmpty() == true) {
				JOptionPane.showMessageDialog(null, "There are no paths to remove!");
			} else {
				pathEditorJFrame();
			}
		});

		// with the sub menu "More"
		JMenu subMenuMore = new JMenu("More");
		subMenuMore.setToolTipText("Save your actual source folder paths and more in a config file for later");
		// and the sub sub menu "Save configuration" >>
		ImageIcon iconSave = new ImageIcon(ImageIO.read(ConceptJFrameGUI.class.getResource("/save_20x20.png")));
		JMenuItem subSubMenuConfigurationSave = new JMenuItem("Save configuration", iconSave);
		subSubMenuConfigurationSave
				.setToolTipText("Saves everything so you can start instantly at the next launch of the program");
		subSubMenuConfigurationSave.addActionListener((ActionEvent event) -> {
			System.out.println("Save the actual configuration (of folders)!");
			actionManager.fileOverWriterConfig();
		});
		// and the sub sub menu "Load configuration" >>
		ImageIcon iconLoad = new ImageIcon(ImageIO.read(ConceptJFrameGUI.class.getResource("/load_20x20.png")));
		JMenuItem subSubMenuConfigurationLoad = new JMenuItem("Load configuration", iconLoad);
		subSubMenuConfigurationLoad.setToolTipText("Load configuration from a configuration file");
		subSubMenuConfigurationLoad.addActionListener((ActionEvent event) -> {
			System.out.println("dialog wich says please restart program - notify if a file even exit before this");
			if (JOptionPane.showConfirmDialog(null,
					"This will overwrite your old configuration! Do you really want to continue?", "Warning",
					JOptionPane.YES_NO_OPTION, JOptionPane.WARNING_MESSAGE) == JOptionPane.YES_OPTION) {
				actionManager.loadConfigData(actionManager.getConfigurationFileOnComputer());
				// now scan again all paths for music videos
				actionManager.updateMusicVideoList();
				updateTable();
			} else {
				System.out.println("\tPlaying was denied by the user.");
			}
		});
		// and the sub sub menu "Export" >>
		ImageIcon iconExport = new ImageIcon(ImageIO.read(ConceptJFrameGUI.class.getResource("/export_20x20.png")));
		JMenu subSubMenuExport = new JMenu("Export");
		subSubMenuExport.setIcon(iconExport);
		subSubMenuExport.setToolTipText("Export your list to the following formats: CSV, HTML");
		// with the sub sub sub menu "Export to CSV" >>
		ImageIcon iconCSV = new ImageIcon(ImageIO.read(ConceptJFrameGUI.class.getResource("/csv_20x20.png")));
		JMenuItem subSubSubMenuExportCSV = new JMenuItem("Export to CSV", iconCSV);
		subSubSubMenuExportCSV.setToolTipText("Export your data to a CSV file (can be imported with Excel)");

		subSubSubMenuExportCSV.addActionListener((ActionEvent event) -> {

			actionManager.exportCsvFile("musicvideolist.csv");
		});
		// with the sub sub sub menu "Export to HTML" >>
		ImageIcon iconHTML = new ImageIcon(ImageIO.read(ConceptJFrameGUI.class.getResource("/html_20x20.png")));
		JMenuItem subSubSubMenuExportHTML = new JMenuItem("Export to HTML", iconHTML);
		subSubSubMenuExportHTML.setToolTipText("Export your data to a HTML file (web browser)");
		subSubSubMenuExportHTML.addActionListener((ActionEvent event) -> {

			actionManager.exportHtmlFile("table.html");
		});
		// and last but not least the info sub sub menu "About" >>
		ImageIcon iconAbout = new ImageIcon(ImageIO.read(ConceptJFrameGUI.class.getResource("/info_20x20.png")));
		JMenuItem subSubMenuAbout = new JMenuItem("About", iconAbout);
		subSubMenuAbout.setToolTipText("About this program");
		subSubMenuAbout.addActionListener((ActionEvent event) -> {
			aboutJFrame();
		});

		// add the menu buttons to the menu bar to the JFrame
		subMenuPath.add(subSubMenuAddSourceFolder);
		subMenuPath.addSeparator();
		subMenuPath.add(subSubMenuRemoveSourceFolder);
		menuBar.add(subMenuPath);
		subMenuMore.add(subSubMenuConfigurationSave);
		subMenuMore.addSeparator();
		subMenuMore.add(subSubMenuConfigurationLoad);
		subMenuMore.addSeparator();
		subSubMenuExport.add(subSubSubMenuExportCSV);
		subSubMenuExport.addSeparator();
		subSubMenuExport.add(subSubSubMenuExportHTML);
		subMenuMore.add(subSubMenuExport);
		subMenuMore.addSeparator();
		subMenuMore.add(subSubMenuAbout);
		menuBar.add(subMenuMore);
		guiMainFrame.setJMenuBar(menuBar);

		model = new DefaultTableModel(actionManager.musicVideoListToTable("  "), actionManager.getColumnNames());
		table = new JTable(model);

		table.getTableHeader().setBackground(Color.LIGHT_GRAY);

		TableColumnModel columnModel = table.getColumnModel();
		columnModel.getColumn(0).setPreferredWidth(5);
		columnModel.getColumn(1).setPreferredWidth(150);
		columnModel.getColumn(2).setPreferredWidth(225);

		((DefaultTableCellRenderer) table.getTableHeader().getDefaultRenderer()).setHorizontalAlignment(JLabel.CENTER);

		DefaultTableCellRenderer centerRenderer = new DefaultTableCellRenderer();
		centerRenderer.setHorizontalAlignment(JLabel.CENTER);
		table.getColumnModel().getColumn(0).setCellRenderer(centerRenderer);

		table.setAutoCreateRowSorter(true);

		// Place the JTable object in a JScrollPane for a scrolling table
		JScrollPane tableScrollPane = new JScrollPane(table);

		guiMainFrame.add(tableScrollPane);

		table.addMouseListener(new java.awt.event.MouseAdapter() {
			@Override
			public void mouseClicked(java.awt.event.MouseEvent evt) {
				int row = table.getSelectedRow();
				actionManager.openMusicVideo(row);
			}
		});

		// add a search bar with filter and input option
		JTextField jtfFilter = new JTextField();
		JPanel panel = new JPanel(new BorderLayout());

		ImageIcon iconSearch = new ImageIcon(ImageIO.read(ConceptJFrameGUI.class.getResource("/search.png")));
		JLabel thumb = new JLabel("  Search for a music video:  ");
		thumb.setIcon(iconSearch);
		thumb.setToolTipText("Type in the field to instantly find your music video");
		panel.add(thumb);

		ImageIcon icon = new ImageIcon(ImageIO.read(ConceptJFrameGUI.class.getResource("/youtube.png")));

		JButton button234 = new JButton(icon);
		button234
				.setToolTipText("Click the button to start a video search on YouTube with the input of the text field");

		button234.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent event) {
				String scannedText = jtfFilter.getText();

				String url = "https://www.youtube.com";
				try {
					url = "https://www.youtube.com/results?search_query=" + URLEncoder.encode(scannedText, "UTF-8");
				} catch (UnsupportedEncodingException e) {
					e.printStackTrace();
				}

				// inspired by http://stackoverflow.com/a/4898607

				if (Desktop.isDesktopSupported()) {
					// Windows
					try {
						Desktop.getDesktop().browse(new URI(url));
					} catch (IOException | URISyntaxException e1) {
						e1.printStackTrace();
					}
				} else {
					// Linux
					Runtime runtime = Runtime.getRuntime();
					try {
						runtime.exec("xdg-open " + url);
						// runtime.exec("/usr/bin/firefox -new-window " + url);
					} catch (IOException e1) {
						e1.printStackTrace();
					}
				}
			}
		});

		panel.add(thumb, BorderLayout.WEST);
		panel.add(button234, BorderLayout.EAST);
		panel.add(jtfFilter, BorderLayout.CENTER);
		panel.setPreferredSize(new Dimension(500, 40));
		guiMainFrame.add(panel, BorderLayout.NORTH);

		// action listener if the enter key was pressed
		Action action = new AbstractAction() {
			// eclipse was this, i dont't like orange light bulbs
			private static final long serialVersionUID = 1L;

			@Override
			public void actionPerformed(ActionEvent e) {

				// get the actual text of the text field
				String scannedText = jtfFilter.getText();

				// check if it is a number (a String only containing digits)
				if (scannedText.matches("[-+]?\\d*\\.?\\d+")) {
					// if yes parse the String to an Integer and
					// open the music video on this position
					actionManager.openMusicVideo(Integer.parseInt(scannedText) - 1);
				} else {
					// when at least on row exists
					if (table.getRowCount() > 0) {
						// algorithm that finds the top result in the actual
						// table and gets the number of it
						actionManager.openMusicVideo((int) table.getValueAt(0, 0) - 1);
					}
				}
			}
		};
		jtfFilter.addActionListener(action);

		// create a row sorter: But NOT to sort the data in the table manually
		// later, this is enabled by default! We need the row sorter for our
		// filter in the search bar
		rowSorter = new TableRowSorter<>(table.getModel());
		table.setRowSorter(rowSorter);

		jtfFilter.getDocument().addDocumentListener(new DocumentListener() {

			@Override
			public void insertUpdate(DocumentEvent e) {
				// update filter if something in text field gets added
				updateFilter(jtfFilter.getText());
			}

			@Override
			public void removeUpdate(DocumentEvent e) {
				// update filter if something in text field gets removed
				updateFilter(jtfFilter.getText());
			}

			@Override
			public void changedUpdate(DocumentEvent arg0) {
				// needs to be implemented, but we don't need it
			}
		});

		// play a random music video button
		ImageIcon iconRandom = new ImageIcon(ImageIO.read(ConceptJFrameGUI.class.getResource("/random.png")));
		JButton randomMusicvideoButton = new JButton("Play a random music video", iconRandom);

		randomMusicvideoButton.setPreferredSize(new Dimension(500, 40));
		randomMusicvideoButton.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent event) {

				int randomNum = actionManager.getRandomNumber(0, actionManager.getMusicVideosList().size());
				String randomSong = actionManager.getMusicVideosList().get(randomNum).getTitle() + " by "
						+ actionManager.getMusicVideosList().get(randomNum).getArtist() + "?";
				System.out.println("Random music video: ...Playing " + randomSong);

				if (JOptionPane.showConfirmDialog(null, "Would you like to play " + randomSong, "Info",
						JOptionPane.YES_NO_OPTION) == JOptionPane.YES_OPTION) {
					actionManager.openMusicVideo(randomNum);
				} else {
					System.out.println("\tPlaying was denied by the user.");
				}
			}
		});
		guiMainFrame.add(randomMusicvideoButton, BorderLayout.SOUTH);

		// make the frame visible for the user (you can do this only if every
		// graphical component was added - otherwise some components will not be
		// displayed.
		guiMainFrame.setVisible(true);

		// when the user wants to close the window (do something)
		guiMainFrame.addWindowListener(new java.awt.event.WindowAdapter() {
			@Override
			public void windowClosing(java.awt.event.WindowEvent windowEvent) {
				// check if there already exist a saved configuration that is
				// different from the actual configuration or if there exist no
				// configuration at all

				boolean fileExistButPathListIsNotTheSame = actionManager
						.fileExists(actionManager.getConfigurationFile())
						&& (!actionManager.configFilePathExtracter().equals(actionManager.getPathList()));
				boolean fileDoesNotExist = !(actionManager.fileExists(actionManager.getConfigurationFile()));
				boolean noPathsExist = actionManager.getPathList().isEmpty();

				if (!noPathsExist && (fileExistButPathListIsNotTheSame || fileDoesNotExist)) {
					// ask the user if he wants to close without saving his
					// actual configuration
					if (JOptionPane.showConfirmDialog(guiMainFrame,
							"Are you sure to close the program without saving your music video folder paths to a configuration file?",
							"Really Closing?", JOptionPane.YES_NO_OPTION,
							JOptionPane.QUESTION_MESSAGE) == JOptionPane.NO_OPTION) {
						actionManager.fileOverWriterConfig();
					}
				}
			}
		});
	}

	/**
	 */
	public void aboutJFrame() {

		JFrame aboutJFrameWindow = new JFrame("About Karaoke Desktop Client [Beta]");
		// set title
		aboutJFrameWindow.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
		// only close on exit - don't end the whole program

		JPanel panel = new JPanel(new BorderLayout());
		panel.setBorder(BorderFactory.createEmptyBorder(10, 10, 10, 10));

		ImageIcon iconLogo;
		JLabel icon = new JLabel();
		try {
			iconLogo = new ImageIcon(ImageIO.read(ConceptJFrameGUI.class.getResource("/logo.png")));
			icon.setIcon(iconLogo);
		} catch (IOException e) {
			e.printStackTrace();
		}

		JLabel author = new JLabel("Autor: Niklas | https://github.com/AnonymerNiklasistanonym ");
		author.addMouseListener((MouseListener) new OpenUrlAction());

		JPanel panel2 = new JPanel(new GridLayout(3, 1));
		panel2.setBorder(BorderFactory.createEmptyBorder(20, 10, 20, 0));

		panel2.add(new JLabel("This program is completely open source on Github"));
		panel2.add(author);
		panel2.add(new JLabel("\u00a9 April 2017"));

		panel.add(icon, BorderLayout.WEST);
		panel.add(panel2, BorderLayout.EAST);
		aboutJFrameWindow.add(panel);

		// make everything fitting perfect
		aboutJFrameWindow.pack();
		// make it visible for the user
		aboutJFrameWindow.setVisible(true);
		// and let it pop up in the middle of the screen
		aboutJFrameWindow.setLocationRelativeTo(null);
		// let nobody change the size of it
		aboutJFrameWindow.setResizable(false);

	}

	/**
	 * Open URL to GitHub profile listener
	 */
	class OpenUrlAction implements MouseListener {

		@Override
		public void mouseClicked(MouseEvent arg0) {
			URI uri = null;
			try {
				uri = new URI("https://github.com/AnonymerNiklasistanonym");
			} catch (URISyntaxException e1) {
			}

			if (Desktop.isDesktopSupported()) {
				try {
					Desktop.getDesktop().browse(uri);
				} catch (IOException e) {
				}
			}

		}

		public void mouseEntered(MouseEvent e) {
		}

		public void mouseExited(MouseEvent e) {
		}

		public void mousePressed(MouseEvent e) {
		}

		public void mouseReleased(MouseEvent e) {
		}
	}

	/**
	 * External JFrame to manage/delete added source folder paths of music
	 * videos. Paths that can be deleted with a click immediately update the
	 * table (/music video list and path list) on their own.
	 */
	public void pathEditorJFrame() {

		JFrame pathEditorWindow = new JFrame("Edit the source folder paths:    >>Close to save changes");
		// set title
		pathEditorWindow.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
		// only close on exit - don't end the whole program

		boolean[] arrayPathIndex = new boolean[actionManager.getPathList().size()];
		Arrays.fill(arrayPathIndex, false);

		// create a grid layout for all paths as a visual button list
		pathEditorWindow.setLayout(new GridLayout(actionManager.getPathList().size(), 1));
		// for all actual saved paths create one button
		for (int i = 0; i < actionManager.getPathList().size(); i++) {

			JButton removePathButton = new JButton();
			removePathButton.setVerticalTextPosition(AbstractButton.CENTER);
			// removePathButton.setHorizontalTextPosition(AbstractButton.LEADING);
			removePathButton.setActionCommand("remove path from path list");
			removePathButton.setPreferredSize(new Dimension(500, 40));

			ImageIcon iconRemove;
			JLabel label = new JLabel("<< Click to remove " + actionManager.getPathList().get(i) + " >>",
					SwingConstants.CENTER);
			try {
				iconRemove = new ImageIcon(ImageIO.read(ConceptJFrameGUI.class.getResource("/remove_20x20.png")));
				label.setIcon(iconRemove);
			} catch (IOException e) {
				e.printStackTrace();
			}

			removePathButton.add(label);

			String pathTextForLater = actionManager.getPathList().get(i).toString();
			int indexOfPath = i;

			removePathButton.addActionListener((ActionEvent event) -> {
				if (arrayPathIndex[indexOfPath] == true) {
					label.setText("<< Click to remove " + pathTextForLater + " >>");
					arrayPathIndex[indexOfPath] = false;

					ImageIcon iconRemove2;
					try {
						iconRemove2 = new ImageIcon(
								ImageIO.read(ConceptJFrameGUI.class.getResource("/remove_20x20.png")));
						label.setIcon(iconRemove2);
					} catch (IOException e) {
						e.printStackTrace();
					}
				} else {
					label.setText(pathTextForLater + " was removed - Click to reverse");
					arrayPathIndex[indexOfPath] = true;

					ImageIcon iconReAdd;
					try {
						iconReAdd = new ImageIcon(ImageIO.read(ConceptJFrameGUI.class.getResource("/undo_20x20.png")));
						label.setIcon(iconReAdd);
					} catch (IOException e) {
						e.printStackTrace();
					}
				}
			});
			pathEditorWindow.add(removePathButton);

			// question the user if he wants this changes to happen when he
			// closes the window and only then delete the paths and update the
			// table
		}

		// now pack all components together for their perfect size
		pathEditorWindow.pack();
		// make it visible for the user
		pathEditorWindow.setVisible(true);
		// and let it pop up in the middle of the screen
		pathEditorWindow.setLocationRelativeTo(null);

		// when the user wants to close the window (do something)
		pathEditorWindow.addWindowListener(new java.awt.event.WindowAdapter() {
			@Override
			public void windowClosing(java.awt.event.WindowEvent windowEvent) {
				boolean changeDetected = false;

				for (boolean a : arrayPathIndex) {
					if (a == true) {
						changeDetected = true;
					}
				}

				if (changeDetected && JOptionPane.showConfirmDialog(null, "Do you really want to save changes?",
						"Important question", JOptionPane.YES_NO_OPTION,
						JOptionPane.WARNING_MESSAGE) == JOptionPane.YES_OPTION) {
					int regulator = 0;
					for (int a = 0; a < arrayPathIndex.length; a++) {
						if (arrayPathIndex[a] == true) {
							actionManager.deletePathFromPathList(a + regulator);
							regulator--;
						}
					}
					updateTable();
				}
			}
		});
	}

	/**
	 * This method removes all rows of our table and updates them with new rows
	 * created of a new read of an up to date music video list.
	 */
	public void updateTable() {

		// delete all actual rows if there are even any rows!
		while (model.getRowCount() > 0) {
			model.removeRow(0);
		}

		// scan each path of the path list after music videos and update so the
		// music video list
		actionManager.updateMusicVideoList();

		// now add for each entry in the new updated music video list a row to
		// the empty table
		for (Object[] a : actionManager.musicVideoListToTable("  ")) {
			model.addRow(a);
		}
	}

	/**
	 * This method updates our TableRowSorter after our filter.
	 * 
	 * @param searchString
	 *            (String | search command from text field)
	 */
	public void updateFilter(String searchString) {
		if (searchString.trim().length() == 0) {
			rowSorter.setRowFilter(null);
		} else {
			rowSorter.setRowFilter(RowFilter.regexFilter("(?i)" + searchString));
		}
	}

	/**
	 * Change the optic if the system OS is Windows
	 */
	public static void windowsDetected() {

		try {
			// UIManager.setLookAndFeel(UIManager.getCrossPlatformLookAndFeelClassName());
			// UIManager.setLookAndFeel("javax.swing.plaf.metal.MetalLookAndFeel");
			// UIManager.setLookAndFeel("com.sun.java.swing.plaf.motif.MotifLookAndFeel");
			if (System.getProperty("os.name").contains("Windows")) {
				UIManager.setLookAndFeel("com.sun.java.swing.plaf.windows.WindowsLookAndFeel");
			}
		} catch (ClassNotFoundException e) {
			e.printStackTrace();
		} catch (InstantiationException e) {
			e.printStackTrace();
		} catch (IllegalAccessException e) {
			e.printStackTrace();
		} catch (UnsupportedLookAndFeelException e) {
			e.printStackTrace();
		}
	}

	/**
	 * This happens when the program gets executed: We create a new
	 * ConceptJFrameGUI and the constructor does the rest :)
	 */
	public static void main(String[] args) {
		windowsDetected();
		// create a new Object of our class
		ConceptJFrameGUI mainFrame = new ConceptJFrameGUI();
		// look after configuration file before starting
		mainFrame.startupConfig();
		// open/show the window
		try {
			mainFrame.createWindow();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

}